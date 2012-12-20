GET /api/v1/auth/
-----------------

.. http:get:: /api/v1/auth/

  Get a list of all tokens of one user.

  :param username: Your username (*required*)
  :param password: Your password (*required*)

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500

  **Example request**:

  .. sourcecode:: bash

      $ curl -X GET -u user:pass https://goo.ncc.unesp.br/api/v1/auth/

  .. sourcecode:: http

      GET /api/v1/auth/ HTTP/1.1
      Authorization: Basic dXNlcjpwYXNz
      User-Agent: curl/7.26.0
      Host: goo.ncc.unesp.br
      Accept: */*

  **Example response**:

  .. sourcecode:: http

      HTTP/1.0 200 OK
      Content-Type: application/json; charset=utf-8

      {
        "meta":
        {
            "limit": 500,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2
        },
        "objects": 
        [ {
            "expire_time": "2013-01-18T15:33:21.615672+00:00",
            "resource_uri": "/api/v1/auth/1/",
            "token": "e2b21252-bb6f-43d5-91b6-0941a9a95558"
           },
           {
            "expire_time": "2013-01-18T15:33:25.706387+00:00",
            "resource_uri": "/api/v1/auth/2/",
            "token": "a18872fd-7566-49de-b016-91ca8fc4d2d3"
           }
        ]
      }

  :statuscode 200: Ok, no error.
  :statuscode 401: Unauthorized
