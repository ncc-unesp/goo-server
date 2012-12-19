#!/usr/bin/env python

import sys, urllib2, json, time, os, tempfile, threading, shlex, uuid, shutil
from subprocess import Popen, PIPE

from zipfile import ZipFile
from glob import glob

STDOUT_SUFFIX = ".stdout"
STDERR_SUFFIX = ".stderr"

# TODO: get this from OSG ENV
STORAGE_SERVER = "gsiftp://se.grid.unesp.br/store/winckler/"

PROGRESS_FREQ = 10 # seconds
CHECKPOINT_FREQ = 20 # seconds

class GooServer:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def do(self, path="dispatcher/", method="GET", data={}):
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
        data = server.do("dispatcher/",
                         "POST", {"time_left": time_left})
        super(Job,self).update(data)

    def __setitem__(self, key, value):
        self.server.do(path="dispatcher/%d/" % self["id"],
                       "PATCH", {key: value})

        super(Job,self).__setitem__(key, value)

def send_files(job, tmp_dir):
    # cd into the directory
    orig_pwd = os.getcwd()
    os.chdir(tmp_dir)

    slug = job['slug']
    output_pack_name = '%s.zip' % slug
    output_pack = ZipFile(output_pack_name, 'w', allowZip64=True)
    output_pack.write(slug + STDOUT_SUFFIX)
    output_pack.write(slug + STDERR_SUFFIX)

    #pack requested files
    for p in job['outputs'].split(","):
        for f in glob(p):
            output_pack.write(f)

    output_pack.close()
    output_pack_size = os.path.getsize(output_pack_name)

    #gridftp copy
    local_url = 'file://' + os.path.abspath(output_pack_name)
    remote_url = STORAGE_SERVER + str(uuid.uuid4) + '.zip'
    devnull = open(os.devnull, 'w')
    ret_code = call(["/usr/bin/globus-url-copy", local_url, remote_url],
                    close_fds=True, stdout=devnull, stderr=devnull)

    if (ret_code != 0):
        raise IOError

    data = {"name": slug + '_output.zip'}
    data["size"] = output_pack_size / 1024**2
    data["url"] = remote_url

    resp = job.server.do("objects/", "POST", data)
    job["output_objs"] = [ resp[resource_uri] ]

    os.chdir(orig_pwd)

def job_loop():
    # get a job
    #TODO: control the time left
    job = Job(server, 400000)

    # create a temporary directory
    # If dir=None in mkstemp, it searchs automatically for TMPDIR and TEMP...
    tmp_path = os.environ.get("GOO_TMPDIR", None)
    tmp_dir = tempfile.mkdtemp(prefix="goo-pilot", dir=tmp_path)

    # get the application.
    # TODO

    # get the input files.
    # TODO

    # execute job
    # missing case name
    stdout_fname = job["slug"] + STDOUT_SUFFIX
    stdout = open(os.path.join(tmp_dir, stdout_fname), 'w')

    stderr_fname = job["slug"] + STDERR_SUFFIX
    stderr = open(os.path.join(tmp_dir, stderr_fname), 'w')

    def execution_thread(job, stdout, stderr):
        args = [ job["executable"], ]
        args.extend(shlex.split(job["args"]))

        process = Popen(args, close_fds=True, stdout=stdout, stderr=stderr)
        process.wait()
        job["return_code"] = process.returncode

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
    except:
        job["status"] = "E"
        # should erase files first?
        return

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
        except urllib2.HTTPError:
            # no more jobs for memory
            print "No more jobs."
            exit(0)
