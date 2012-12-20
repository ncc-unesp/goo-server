GET /api/v1/jobs/(id)
---------------------

.. http:get:: /api/v1/jobs/(int:id)/

  Get info about an user job.

  :param id: job id

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500
  :query token: Your API token (*required*)

  **Example request**:

  .. sourcecode:: bash

      $ curl -X GET https://goo.ncc.unesp.br/api/v1/jobs/1/?token=e2b21252-bb6f-43d5-91b6-0941a9a95558

  .. sourcecode:: http

      GET /api/v1/jobs/1/ HTTP/1.1
      User-Agent: curl/7.26.0
      Host: goo.ncc.unesp.br
      Accept: */*

  **Example response**:

  .. sourcecode:: http

      HTTP/1.0 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "meta": {
              "limit": 500, 
              "next": null, 
              "offset": 0, 
              "previous": null, 
              "total_count": 1
          }, 
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
              }
          ]
      }

  :statuscode 200: Ok, no error
  :statuscode 401: Unauthorized
