POST /api/v1/jobs/
------------------

.. http:post:: /api/v1/jobs/

  Submmit a job to queue.

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500
  :query token: Your API token (*required*)

  **Example request**:

  .. sourcecode:: bash

      $ data='{"app":"/api/v1/apps/33/", "args": "10", "executable": "/bin/sleep", "name":"job2" }'
      $ curl -H "Content-Type: application/json"  -X POST -d $data https://goo.ncc.unesp.br/api/v1/jobs/?token=e2b21252-bb6f-43d5-91b6-0941a9a95558

  .. sourcecode:: http

      POST /api/v1/jobs/ HTTP/1.1
      User-Agent: curl/7.26.0
      Host: goo.ncc.unesp.br
      Accept: */*

  **Example response**:

  .. sourcecode:: http

      HTTP/1.0 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "app": "/api/v1/apps/33/", 
          "app_name": "Python 2.7 MPI", 
          "args": "10", 
          "checkpoints": "", 
          "executable": "/bin/sleep", 
          "id": 4, 
          "inputs": "", 
          "name": "job2", 
          "outputs": "", 
          "priority": 0, 
          "progress": 0, 
          "progress_string": "", 
          "resource_uri": "/api/v1/jobs/4/", 
          "status": "P"
      }

  :statuscode 201: Created
  :statuscode 401: Unauthorized
