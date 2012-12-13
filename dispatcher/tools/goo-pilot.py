#!/usr/bin/env python

import sys, urllib2, json, time, os, tempfile, threading, shlex
from subprocess import Popen, PIPE

STDOUT_SUFFIX = ".stdout"
STDERR_SUFFIX = ".stderr"

PROGRESS_FREQ = 10 # seconds
CHECKPOINT_FREQ = 20 # seconds

class GooServer:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def do(self, path="", method="GET", data={}):
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
        data = server.do(path="",
                         method="POST",
                         data={"time_left": time_left})
        super(Job,self).update(data)

    def __setitem__(self, key, value):
        self.server.do(path="%d/" % self["id"],
                       method="PATCH",
                       data={key: value})

        super(Job,self).__setitem__(key, value)

def job_loop():
    # get a job
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
    stdout = open(os.path.join(tmp_dir, STDOUT_SUFFIX), 'w')
    stderr = open(os.path.join(tmp_dir, STDERR_SUFFIX), 'w')

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
    # TODO

    #remove temporary directory
    # TODO
    
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
