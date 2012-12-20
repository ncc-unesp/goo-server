GET /api/v1/apps/(id)/
----------------------

.. http:get:: /api/v1/apps/(int:id)/

  Get info about an application.

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500
  :query token: User token (**required**)

  **Example request**:

  .. sourcecode:: bash

      $ curl -X GET https://goo.ncc.unesp.br/api/v1/apps/1/?token=1fbec48e-50d0-4b6a-b8af-bb230a339011

  .. sourcecode:: http

      GET /api/v1/apps/1/ HTTP/1.1
      User-Agent: curl/7.26.0
      Host: goo.ncc.unesp.br
      Accept: */*

  **Example response**:

  .. sourcecode:: http

      HTTP/1.0 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "app_obj": null, 
          "args": "args", 
          "checkpoints": "", 
          "executable": "", 
          "id": "1", 
          "inputs": "", 
          "multi_hosts": false, 
          "multi_thread": false, 
          "name": "BEAST 1.6.1 Serial", 
          "outputs": "", 
          "resource_uri": "/api/v1/apps/1/", 
          "shared_fs": true
      }

  :statuscode 200: Ok, no error
  :statuscode 401: Unauthorized
  :statuscode 404: Not found
