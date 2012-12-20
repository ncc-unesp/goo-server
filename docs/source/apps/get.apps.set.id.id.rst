GET /api/v1/apps/set/(first);(last)/
------------------------------------

.. http:get:: /api/v1/apps/set/(int:first)/(int:last)/

  Get a set of applications supported by NCC - UNESP.

  :param first: Token id (not hash) (*required*)
  :param last: Token id (not hash) (*required*)

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500
  :query token: User token (**required**)

  **Example request**:

  .. sourcecode:: bash

      $ curl -X GET https://goo.ncc.unesp.br/api/v1/apps/set/1;3/?token=1fbec48e-50d0-4b6a-b8af-bb230a339011

  .. sourcecode:: http

      GET /api/v1/apps/set/1;3/ HTTP/1.1
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
                  "id": "1", 
                  "multi_hosts": false, 
                  "multi_thread": false, 
                  "name": "BEAST 1.6.1 Serial", 
                  "resource_uri": "/api/v1/apps/1/"
              }, 
              {
                  "id": "2", 
                  "multi_hosts": false, 
                  "multi_thread": true, 
                  "name": "BEAST 1.6.1 SMP", 
                  "resource_uri": "/api/v1/apps/2/"
              }, 
              {
                  "id": "3", 
                  "multi_hosts": true, 
                  "multi_thread": false, 
                  "name": "Clustalw 1.82 MPI", 
                  "resource_uri": "/api/v1/apps/3/"
              }, 
          ]
      }

  :statuscode 200: Ok, no error
  :statuscode 401: Unauthorized
