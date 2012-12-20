GET /api/v1/token/
------------------

.. http:get:: /api/v1/token/

  Check if a token is valid, if it is, a expire time will be returned, if not a 
  HTTP 401.

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500
  :query token: Your API token (*required*)

  **Example request**:

  .. sourcecode:: bash

      $ curl -X GET https://goo.ncc.unesp.br/api/v1/token/?token=e2b21252-bb6f-43d5-91b6-0941a9a95558

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
          "expire_time": "2013-01-18T14:57:40.879713"
      }

  :statuscode 200: Ok, no error
  :statuscode 401: Unauthorized
