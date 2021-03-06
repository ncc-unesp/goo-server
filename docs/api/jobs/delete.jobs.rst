DELETE /api/v1/jobs/
--------------------

.. http:delete:: /api/v1/jobs/

  Remove **ALL** jobs from the queue.

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500
  :query token: Your API token (*required*)

  **Example request**:

  .. sourcecode:: bash

      $ curl -X DELETE https://goo.ncc.unesp.br/api/v1/jobs/?token=1fbec48e-50d0-4b6a-b8af-bb230a339011

  .. sourcecode:: http

      DELETE /api/v1/jobs/ HTTP/1.1
      User-Agent: curl/7.26.0
      Host: goo.ncc.unesp.br
      Accept: */*

  **Example response**:

  .. sourcecode:: http

      HTTP/1.0 204 NO CONTENT
      Content-Type: text/html; charset=utf-8

  :statuscode 204: No Content (Removed with success)
  :statuscode 401: Unauthorized
