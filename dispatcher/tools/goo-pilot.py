#!/usr/bin/env python

import sys, urllib2, json, time

class GooServer:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def do(self, path="", method="GET", data={}):
        url = "%s%s?token=%s" % (self.base_url, path, self.token)
        request = RequestWithMethod(method, url=url)
        request.add_header("Content-Type", "application/json")
        request.add_data(json.dumps(data))

        return json.loads(urllib2.urlopen(request).read())

class RequestWithMethod(urllib2.Request):
  def __init__(self, method, *args, **kwargs):
    self._method = method
    urllib2.Request.__init__(self, *args, **kwargs)

  def get_method(self):
    return self._method
    
def exec_loop():
    # get a job
    job = server.do(method="POST", data={"time_left": 400000})
    print job

    time.sleep(30)

    # update info
    job = server.do(path="%d/" % job["id"], method="PATCH", data={"status": "P"})
    print job

if __name__ == "__main__":
    # get server url and token from command line
    server = GooServer(sys.argv[1], sys.argv[2])

    while True:
        exec_loop()



