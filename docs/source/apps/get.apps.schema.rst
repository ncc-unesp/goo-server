GET /api/v1/apps/schema/
------------------------

.. http:get:: /api/v1/apps/schema/

  Get app schema info.

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500
  :query token: User token (**required**)

  **Example request**:

  .. sourcecode:: bash

      $ curl -X GET https://goo.ncc.unesp.br/api/v1/auth/schema/?token=1fbec48e-50d0-4b6a-b8af-bb230a339011

  .. sourcecode:: http

      GET /api/v1/auth/schema/ HTTP/1.1
      User-Agent: curl/7.26.0
      Host: goo.ncc.unesp.br
      Accept: */*

  **Example response**:

  .. sourcecode:: http

      HTTP/1.0 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "allowed_detail_http_methods": [
              "get"
          ], 
          "allowed_list_http_methods": [
              "get"
          ], 
          "default_format": "application/json", 
          "default_limit": 500, 
          "fields": {
              "app_obj": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "help_text": "A single related resource. Can be either a URI or set of nested resource data.", 
                  "nullable": true, 
                  "readonly": false, 
                  "type": "related", 
                  "unique": false
              }, 
              "args": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "string", 
                  "unique": false
              }, 
              "checkpoints": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "string", 
                  "unique": false
              }, 
              "executable": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "string", 
                  "unique": false
              }, 
              "id": {
                  "blank": false, 
                  "default": "", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "string", 
                  "unique": true
              }, 
              "inputs": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "string", 
                  "unique": false
              }, 
              "multi_hosts": {
                  "blank": false, 
                  "default": "False", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "boolean", 
                  "unique": false
              }, 
              "multi_thread": {
                  "blank": false, 
                  "default": "False", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "boolean", 
                  "unique": false
              }, 
              "name": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "string", 
                  "unique": false
              }, 
              "outputs": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "string", 
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
              "shared_fs": {
                  "blank": false, 
                  "default": "False", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "boolean", 
                  "unique": false
              }
          }
      }

  :statuscode 200: Ok, no error
  :statuscode 401: Unauthorized
