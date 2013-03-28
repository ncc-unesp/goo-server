#!/usr/bin/env python
import sys, urllib2, urllib, json, time, os, tempfile, threading, shlex, uuid, shutil
from subprocess import Popen, PIPE, call, check_output, CalledProcessError

from zipfile import ZipFile
from glob import glob

STDOUT_SUFFIX = ".stdout"
STDERR_SUFFIX = ".stderr"

GRIDFTP = "globus-url-copy"

PROGRESS_FREQ = 10 # seconds
CHECKPOINT_FREQ = 20 # seconds

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

    def __setitem__(self, key, value):
        self.server.do("/api/v1/dispatcher/%d/" % self["id"], "PATCH", {key: value})

        super(Job,self).__setitem__(key, value)

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

        # check for lock and move
        if not os.path.exists(control_file):
            os.rename(tmp_dir, app_path)
            # create .installed
            open(control_file, 'w').close()
        else:
            shutil.rmtree(tmp_dir)

    return app_path

def set_dataserver(gooserver):
    if not hasattr(gooserver, 'dataproxy'):
        obj_servers = gooserver.do('/api/v1/dataproxyserver/')
        # get first server
        gooserver.dataproxy = obj_servers["objects"][0]["url"]

def download_file(src_uri, dst_dir, gooserver):
    # hack: also accept src_uri as dict to avoid additional query
    #   if input_objs full hydrated
    if type(src_uri) == dict:
        src_obj = src_uri
    else:
        src_obj = gooserver.do(src_uri)
    dst_path = os.path.join(os.path.abspath(dst_dir), src_obj['name'])

    # try download via GSIFTP
    src_url = src_obj['url']
    dst_url = 'file://' + dst_path

    NULL = open('/dev/null', 'w')
    ret_code = call([GRIDFTP, "-q", src_url, dst_url], 
                    stdout=NULL, stderr=NULL, close_fds=True)
    if (ret_code != 0):
        # error via GSIFTP
        # trying HTTP
        set_dataserver(gooserver)
        src_url = "%sapi/v1/dataproxy/objects/%d/?token=%s" % \
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

    # gridftp copy
    STORAGE_SERVER = os.environ.get("OSG_DEFAULT_SE", "se.grid.unesp.br")
    local_url = 'file://' + src_file
    remote_url = "gsiftp://%s/store/gridunesp/goo/%s.zip" % (STORAGE_SERVER,
                                                             str(uuid.uuid4()))

    NULL = open('/dev/null', 'w')
    ret_code = call([GRIDFTP, "-q", local_url, remote_url],
                    stdout=NULL, stderr=NULL, close_fds=True)

    if (ret_code != 0):
        # error via GSIFTP
        # trying HTTP
        set_dataserver(gooserver)
        # using curl to avoid memory copy and multipart-form mess
        request_url = "%sapi/v1/dataproxy/objects/?token=%s" % \
                        (gooserver.dataproxy, gooserver.token)
        args = "curl -s -F size=%d -F name=%s -F file=@%s %s" % \
                 (size, basename, src_file, request_url)
        try:
            resp = check_output(args, shell=True)
            return json.loads(resp)["resource_uri"]
        except CalledProcessError:
            raise ObjectDownloadError

    else:
        # GSIFTP upload ok. Save meta data.
        data = {"name": base, "size": size, "url": remote_url}
        resp = gooserver.do("/api/v1/objects/", "POST", data)
        return resp["resource_uri"]

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
    for p in job['outputs'].split(","):
        for f in glob(p):
            output_pack.write(f)

    output_pack.close()

    output_pack_uri = upload_file(output_pack_name, job.server)
    job["output_objs"] = [ output_pack_uri ]

    os.chdir(orig_pwd)

def job_loop():
    # get a job
    #TODO: control the time left
    job = Job(server, 400000)

    # create a temporary directory
    # If dir=None in mkstemp, it searchs automatically for TMPDIR and TEMP...
    tmp_path = os.environ.get("GOO_TMPDIR", None)
    tmp_dir = tempfile.mkdtemp(prefix="goo-pilot-", dir=tmp_path)

    orig_pwd = os.getcwd()
    os.chdir(tmp_dir)

    try:
        # get the application.
        install_app(job)
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
    stdout_fname = job["slug"] + STDOUT_SUFFIX
    stdout = open(os.path.join(tmp_dir, stdout_fname), 'w')

    stderr_fname = job["slug"] + STDERR_SUFFIX
    stderr = open(os.path.join(tmp_dir, stderr_fname), 'w')

    def execution_thread(job, stdout, stderr):
        args = [ job["executable"], ]

        job_args = job["args"]

        # http://bugs.python.org/issue6988
        if sys.version_info < (2,7):
            job_args = str(job_args)

        args.extend(shlex.split(job_args))

        process = Popen(args, close_fds=True, stdout=stdout, stderr=stderr)
        process.wait()
        job["return_code"] = process.returncode

        #set progress to 100% if ret_code = 0
        if process.returncode == 0:
            job["progress"] = 100

    execution = threading.Thread(target=execution_thread,
                                 args=(job, stdout, stderr))

    last_progress = time.clock()
    last_checkpoint = time.clock()

    execution.start()

    while execution.is_alive():
        if (time.clock() - last_progress) > PROGRESS_FREQ:
            # do progress
            # TODO
            print "do progress"
            last_progress = time.clock()

        if (time.clock() - last_checkpoint) > CHECKPOINT_FREQ:
            # copy checkpoint
            # TODO
            print "copy checkpoint"
            last_checkpoint = time.clock()

        execution.join(60)

    # send output files
    stdout.close()
    stderr.close()

    try:
        send_files(job, tmp_dir)
    except ObjectUploadError:
        job["status"] = "E"
        # should erase files first?
        return

    os.chdir(orig_pwd)

    # remove temporary directory
    #shutil.rmtree(tmp_dir)
    
    # update info
    job["status"] = "C"

if __name__ == "__main__":
    # get server url and token from command line
    server = GooServer(sys.argv[1], sys.argv[2])

    while True:
        try:
            job_loop()
        except NoJobError:
            print "No more jobs."
            exit(0)
