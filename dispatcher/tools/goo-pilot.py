#!/usr/bin/env python
import sys, urllib2, urllib, json, time, os, tempfile, threading, shlex, uuid, shutil, stat
from string import Template
from subprocess import Popen, PIPE, call

from zipfile import ZipFile
from glob import glob

STDOUT_SUFFIX = ".stdout"
STDERR_SUFFIX = ".stderr"

PROGRESS_FREQ = 300 # seconds
CHECKPOINT_FREQ = 7200 # seconds

class NoJobError(Exception):
    pass

class ObjectUploadError(Exception):
    pass

class ObjectDownloadError(Exception):
    pass

class GooServer:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def do(self, path="/api/v1/dispatcher/", method="GET", data={}):
        url = "%s%s?token=%s" % (self.base_url, path, self.token)
        request = self.RequestWithMethod(method, url=url)
        request.add_header("Content-Type", "application/json")
        request.add_data(json.dumps(data))

        return json.loads(urllib2.urlopen(request).read())

    def set_dataserver(self):
        if not hasattr(self, 'dataproxy'):
            obj_servers = self.do('/api/v1/dataproxyserver/')
            # get first server
            self.dataproxy = obj_servers["objects"][0]["url"]

    class RequestWithMethod(urllib2.Request):
      def __init__(self, method, *args, **kwargs):
        self._method = method
        urllib2.Request.__init__(self, *args, **kwargs)

      def get_method(self):
        return self._method

class Job(dict):
    def __init__(self, server, time_left, *args, **kw):
        super(Job,self).__init__(*args, **kw)

        self.server = server
        # try to get a job
        try:
            data = server.do("/api/v1/dispatcher/", "POST", {"time_left": time_left})
        except urllib2.HTTPError:
            raise NoJobError

        super(Job,self).update(data)
        self._expand_templates()

    def __setitem__(self, key, value):
        self.server.do("/api/v1/dispatcher/%d/" % self["id"], "PATCH", {key: value})
        super(Job,self).__setitem__(key, value)

    def _expand_templates(self):
        for key, value in self.iteritems():
            if type(value) == str or type(value) == unicode:
                new = Template(value).safe_substitute(self)
                # direct call parent setitem to avoid
                # update job info with template expantion
                super(Job,self).__setitem__(key, new)

def install_app(job):
    sys_app_dir = os.environ.get("OSG_APP", tempfile.gettempdir())
    install_dir = os.path.join(sys_app_dir, "gridunesp", "goo")
    app = job['application']

    if not app['_app_obj']:
        return False

    app_path = os.path.join(install_dir, str(app['id']))
    control_file = os.path.join(app_path, '.installed')

    if not os.path.exists(control_file):
        # create installation directory
        if not os.path.isdir(install_dir):
            os.makedirs(install_dir)

        # create a temporary directory
        tmp_dir = tempfile.mkdtemp("-zip", ".", install_dir)

        # download
        zip_file = download_file(app['_app_obj'], tmp_dir, job.server)

        # extract
        ZipFile(zip_file, 'r').extractall(tmp_dir)
        os.remove(zip_file)

        # set execution permissions
        for d in ['bin', 'hooks']:
            dpath = os.path.join(tmp_dir, d)
            for f in os.listdir(dpath):
                fpath = os.path.join(dpath, f)
                os.chmod(fpath, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)

        # check for lock and move
        if not os.path.exists(control_file):
            os.rename(tmp_dir, app_path)
            # create .installed
            open(control_file, 'w').close()
        else:
            shutil.rmtree(tmp_dir)

    return app_path

def download_file(src_uri, dst_dir, gooserver):
    # hack: also accept src_uri as dict to avoid additional query
    #   if input_objs full hydrated
    if type(src_uri) == dict:
        src_obj = src_uri
    else:
        src_obj = gooserver.do(src_uri)
    dst_path = os.path.join(os.path.abspath(dst_dir), src_obj['name'])

    # trying HTTP
    gooserver.set_dataserver()
    src_url = "%sapi/v1/dataproxy/dataobjects/%d/?token=%s" % \
                 (gooserver.dataproxy, src_obj['id'], gooserver.token)
    try:
        urllib.urlretrieve(src_url, dst_path)
    except IOError:
        ObjectDownloadError

    return dst_path

def get_files(job, tmp_dir):
    for i in job['input_objs']:
        fname = download_file(i, tmp_dir, job.server)

        if os.path.splitext(fname)[1].lower() == ".zip":
            ZipFile(fname, 'r').extractall(tmp_dir)
            os.remove(fname)

def upload_file(src_file, gooserver):
    src_file = os.path.abspath(src_file)

    size = os.path.getsize(src_file)
    basename = os.path.basename(src_file)

    # trying HTTP
    gooserver.set_dataserver()
    # using curl to avoid memory copy and multipart-form mess
    request_url = "%sapi/v1/dataproxy/dataobjects/?token=%s" % \
                    (gooserver.dataproxy, gooserver.token)
    # -k (insecure) to avoid certificate error
    args = "curl -k -s -F size=%d -F name=%s -F file=@%s %s" % \
             (size, basename, src_file, request_url)

    process = Popen(args, close_fds=True, stdout=PIPE, stderr=PIPE, shell=True)
    (stdout, stderr) = process.communicate()
    if process.returncode == 0:
        return json.loads(stdout)["resource_uri"]
    else:
        raise ObjectUploadError

def send_files(job, tmp_dir):
    # cd into the directory
    orig_pwd = os.getcwd()
    os.chdir(tmp_dir)

    slug = job['slug']
    output_pack_name = '%s-output.zip' % slug
    output_pack = ZipFile(output_pack_name, 'w', allowZip64=True)
    output_pack.write(slug + STDOUT_SUFFIX)
    output_pack.write(slug + STDERR_SUFFIX)

    #pack requested files
    for p in job['outputs'].split():
        for f in glob(p):
            output_pack.write(f)

    output_pack.close()

    output_pack_uri = upload_file(output_pack_name, job.server)
    job["output_objs"] = [ output_pack_uri ]

    os.chdir(orig_pwd)

def job_loop(remaining_time):
    # get a job
    job = Job(server, remaining_time)

    # create a temporary directory
    # If dir=None in mkstemp, it searchs automatically for TMPDIR and TEMP...
    tmp_path = os.environ.get("GOO_TMPDIR", None)
    tmp_dir = tempfile.mkdtemp(prefix="goo-pilot-", dir=tmp_path)

    orig_pwd = os.getcwd()
    os.chdir(tmp_dir)

    try:
        # get the application.
        app_path = install_app(job)
    except ObjectDownloadError:
        job["status"] = "E"
        return

    try:
        # get the input files.
        get_files(job, tmp_dir)
    except ObjectDownloadError:
        job["status"] = "E"
        return

    # execute job
    # missing case name
    stdout = job["slug"] + STDOUT_SUFFIX
    stderr = job["slug"] + STDERR_SUFFIX

    # set environment (same for the job and the progress hook)
    env = os.environ.copy()
    if app_path:
            env["PATH"] = "%s/bin:%s" % (app_path, env.get("PATH",""))
            env["LD_LIBRARY_PATH"] = "%s/lib:%s" % \
                                       (app_path, env.get("LD_LIBRARY_PATH",""))
    env["GOO_NAME"] = job["slug"]
    env["GOO_STDOUT"] = stdout
    env["GOO_STDERR"] = stderr
    env["GOO_ARGS"] = job["args"]

    def execution_thread(job, app_path, env, stdout, stderr):
        # args
        if job["executable"]:
            args = [ job["executable"] ]
        else:
            args = [ "%s/hooks/execute" % app_path ]

        job_args = job["args"]

        # http://bugs.python.org/issue6988
        if sys.version_info < (2,7):
            job_args = str(job_args)

        args.extend(shlex.split(job_args))

        stdout_obj = open(stdout, 'w')
        stderr_obj = open(stderr, 'w')

        process = Popen(args, stdout=stdout_obj, stderr=stderr_obj,
                        close_fds=True, env=env)
        process.wait()
        job["return_code"] = process.returncode

        stdout_obj.close()
        stderr_obj.close()

    execution = threading.Thread(target=execution_thread,
                                 args=(job, app_path, env, stdout, stderr))

    last_progress = time.time()
    last_checkpoint = time.time()

    execution.start()

    while execution.is_alive():
        if (time.time() - last_progress) > PROGRESS_FREQ:
            # progress % and ETA
            update_progress(job, app_path, env)
            last_progress = time.clock()

        if (time.time() - last_checkpoint) > CHECKPOINT_FREQ:
            # copy checkpoint
            # TODO
            last_checkpoint = time.clock()

        execution.join(60)

    # force a last update
    update_progress(job, app_path, env)
    #set progress to 100% if ret_code = 0
    if job["return_code"] == 0:
        job["progress"] = 100

    # send output files
    try:
        send_files(job, tmp_dir)
    except ObjectUploadError:
        job["status"] = "E"
        # should erase files first?
        return

    os.chdir(orig_pwd)

    # remove temporary directory
    shutil.rmtree(tmp_dir)

    # update info
    job["status"] = "C"

def update_progress(job, app_path, env):
    # progress % and ETA
    hook = "%s/hooks/progress" % app_path
    progress = None
    eta = None
    if os.path.exists(hook):
        process = Popen(hook, stdout=PIPE, close_fds=True, env=env)
        (stdout, stderr) = process.communicate()
        if process.returncode == 0:
            try:
                progress = int(stdout.splitlines()[0])
                eta = int(stdout.splitlines()[1])
            except (ValueError, IndexError):
                pass
    if progress != None:
        job["progress"] = progress
    if eta != None:
        job["eta"] = eta

    # just send a keep alive
    if (not progress) and (not eta):
        job["status"] = "R"

    # tail
    hook = "%s/hooks/log" % app_path
    if os.path.exists(hook):
        process = Popen(hook, stdout=PIPE, close_fds=True, env=env)
        (stdout, stderr) = process.communicate()
        if process.returncode == 0:
            job["progress_string"] = stdout[:6144]

if __name__ == "__main__":
    # get server url and token from command line
    server = GooServer(sys.argv[1], sys.argv[2])

    # get lease time
    lease_time = int(os.environ.get("GOO_LEASE_TIME", 86400))
    limit_time = time.time() + lease_time

    while True:
        try:
            remaining_time = limit_time - time.time()
            job_loop(remaining_time)
        except NoJobError:
            print "No more jobs."
            exit(0)
