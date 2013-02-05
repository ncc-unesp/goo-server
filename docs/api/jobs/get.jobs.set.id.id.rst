GET /api/v1/jobs/set/(first);(last)/
------------------------------------

.. http:get:: /api/v1/jobs/set/(int:first);(int:last)/

  Get a set of all jobs of one user.

  :param first: first job id (*required*)
  :param last: last job id (*required*)

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500
  :query token: Your API token (*required*)

  **Example request**:

  .. sourcecode:: bash

      $ curl -X GET https://goo.ncc.unesp.br/api/v1/jobs/set/1;2/?token=e2b21252-bb6f-43d5-91b6-0941a9a95558

  .. sourcecode:: http

      GET /api/v1/jobs/set/1;2/ HTTP/1.1
      User-Agent: curl/7.26.0
      Host: goo.ncc.unesp.br
      Accept: */*

  **Example response**:

  .. sourcecode:: http

      HTTP/1.0 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "objects": [
              {
                  "app": "/api/v1/apps/1/", 
                  "app_name": "BEAST 1.6.1 Serial", 
                  "args": "", 
                  "checkpoints": "", 
                  "executable": "", 
                  "id": "1", 
                  "inputs": "", 
                  "name": "Job Test", 
                  "outputs": "", 
                  "priority": 0, 
                  "progress": 0, 
                  "progress_string": "", 
                  "resource_uri": "/api/v1/jobs/1/", 
                  "status": "P"
              },
          "objects": [
              {
                  "app": "/api/v1/apps/1/", 
                  "app_name": "BEAST 1.6.1 Serial", 
                  "args": "", 
                  "checkpoints": "", 
                  "executable": "", 
                  "id": "2", 
                  "inputs": "", 
                  "name": "Job Test 2",
                  "outputs": "", 
                  "priority": 3, 
                  "progress": 0, 
                  "progress_string": "", 
                  "resource_uri": "/api/v1/jobs/2/",
                  "status": "R"
              }

          ]
      }

  :statuscode 200: Ok, no error
  :statuscode 401: Unauthorized
