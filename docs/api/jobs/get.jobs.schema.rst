GET /api/v1/jobs/schema/
------------------------

.. http:get:: /api/v1/jobs/schema/

  Get a jobs schema info.

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500
  :query token: Your API token (*required*)

  **Example request**:

  .. sourcecode:: bash

      $ curl -X GET https://goo.ncc.unesp.br/api/v1/jobs/schema/?token=e2b21252-bb6f-43d5-91b6-0941a9a95558

  .. sourcecode:: http

      GET /api/v1/jobs/schema/ HTTP/1.1
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
              "patch", 
              "delete"
          ], 
          "allowed_list_http_methods": [
              "get", 
              "post"
          ], 
          "default_format": "application/json", 
          "default_limit": 500, 
          "fields": {
              "app": {
                  "blank": false, 
                  "default": "No default provided.", 
                  "help_text": "A single related resource. Can be either a URI or set of nested resource data.", 
                  "nullable": true, 
                  "readonly": false, 
                  "related_type": "to_one", 
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
              "create_time": {
                  "blank": true, 
                  "default": true, 
                  "help_text": "A date & time as a string. Ex: \"2010-11-10T03:07:43\"", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "datetime", 
                  "unique": false
              }, 
              "diskspace_in_use": {
                  "blank": false, 
                  "default": 0, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "integer", 
                  "unique": false
              }, 
              "disk_requirement": {
                  "blank": false, 
                  "default": 2048, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "integer", 
                  "unique": false
              }, 
              "end_time": {
                  "blank": false, 
                  "default": null, 
                  "help_text": "A date & time as a string. Ex: \"2010-11-10T03:07:43\"", 
                  "nullable": true, 
                  "readonly": false, 
                  "type": "datetime", 
                  "unique": false
              }, 
              "eta": {
                  "blank": false, 
                  "default": null, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": true, 
                  "readonly": false, 
                  "type": "integer", 
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
              "hosts": {
                  "blank": false, 
                  "default": 1, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "integer", 
                  "unique": false
              }, 
              "id": {
                  "blank": true, 
                  "default": "", 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "integer", 
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
              "memory_in_use": {
                  "blank": false, 
                  "default": 0, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "integer", 
                  "unique": false
              }, 
              "memory_requirement": {
                  "blank": false, 
                  "default": 2048, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "integer", 
                  "unique": false
              }, 
              "modification_time": {
                  "blank": true, 
                  "default": true, 
                  "help_text": "A date & time as a string. Ex: \"2010-11-10T03:07:43\"", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "datetime", 
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
              "pph": {
                  "blank": false, 
                  "default": 1, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "integer", 
                  "unique": false
              }, 
              "priority": {
                  "blank": false, 
                  "default": 0, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "integer", 
                  "unique": false
              }, 
              "progress": {
                  "blank": false, 
                  "default": 0, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "integer", 
                  "unique": false
              }, 
              "progress_string": {
                  "blank": false, 
                  "default": "", 
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
              "restart": {
                  "blank": true, 
                  "default": "False", 
                  "help_text": "Boolean data. Ex: True", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "boolean", 
                  "unique": false
              }, 
              "return_code": {
                  "blank": false, 
                  "default": null, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": true, 
                  "readonly": false, 
                  "type": "integer", 
                  "unique": false
              }, 
              "start_time": {
                  "blank": false, 
                  "default": null, 
                  "help_text": "A date & time as a string. Ex: \"2010-11-10T03:07:43\"", 
                  "nullable": true, 
                  "readonly": false, 
                  "type": "datetime", 
                  "unique": false
              }, 
              "status": {
                  "blank": false, 
                  "default": "P", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "string", 
                  "unique": false
              }, 
              "ttl": {
                  "blank": false, 
                  "default": 43200, 
                  "help_text": "Integer data. Ex: 2673", 
                  "nullable": false, 
                  "readonly": false, 
                  "type": "integer", 
                  "unique": false
              }
          }
      }

  :statuscode 200: Ok, no error
  :statuscode 401: Unauthorized
