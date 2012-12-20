GET /api/v1/auth/schema/
------------------------

.. http:get:: /api/v1/auth/schema/

  Get a auth schema info.

  :param username: Your username (*required*)
  :param password: Your password (*required*)

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500

  **Example request**:

  .. sourcecode:: bash

      $ curl -X GET -u user:pass https://goo.ncc.unesp.br/api/v1/auth/schema/

  .. sourcecode:: http

      GET /api/v1/auth/schema/ HTTP/1.1
      Authorization: Basic dXNlcjpwYXNz
      User-Agent: curl/7.26.0
      Host: goo.ncc.unesp.br
      Accept: */*

  **Example response**:

  .. sourcecode:: http

      HTTP/1.0 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "allowed_detail_http_methods": [
              "get", 
              "post", 
              "delete"
          ], 
          "allowed_list_http_methods": [
              "get", 
              "post", 
              "delete"
          ], 
          "default_format": "application/json", 
          "default_limit": 500, 
          "fields": {
              "expire_time": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "datetime", 
                  "unique": false
              }, 
              "resource_uri": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "nullable": false, 
                  "readonly": true, 
                  "type": "string", 
                  "unique": false
              }, 
              "token": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "string", 
                  "unique": false
              }
          }
      }

  :statuscode 200: Ok, no error
  :statuscode 401: Unauthorized
