POST /api/v1/auth/
------------------

.. http:post:: /api/v1/auth/

  Request a new token. All tokens have an expiration period of 30 days.

  :param username: Your username (*required*)
  :param password: Your password (*required*)

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500

  **Example request**:

  .. sourcecode:: bash

      $ curl -H "Content-Type: application/json"  -X POST -d '{}' -u user:pass https://goo.ncc.unesp.br/api/v1/auth/

  .. sourcecode:: http

      POST /api/v1/auth/ HTTP/1.1
      Authorization: Basic cm9vdDoxMjM=
      User-Agent: curl/7.26.0
      Host: goo.ncc.unesp.br
      Accept: */*
      Content-Type: application/json
      Content-Length: 2

  **Example response**:

  .. sourcecode:: http

      HTTP/1.0 201 CREATED
      Content-Type: application/json; charset=utf-8
      Location: https://goo.ncc.unesp.br/api/v1/auth/4/

      {
        "expire_time": "2013-01-18T16:20:29.088037+00:00", 
        "resource_uri": "/api/v1/auth/4/", 
        "token": "7b96dc8f-a1c4-4def-9d11-171974c557e3"
      }


  :statuscode 201: Created
  :statuscode 401: Unauthorized
