DELETE /api/v1/auth/(id)/
-------------------------

.. http:delete:: /api/v1/auth/(int:id)/

  Revoke **a specific** token of one user.

  :param username: Your username (*required*)
  :param password: Your password (*required*)
  :param id: Token id (not hash) (*required*)

  :query format: return format, one of ``json``, ``xml``. Default is ``json``.
  :query limit: limit result queryset. Default is 500

  **Example request**:

  .. sourcecode:: bash

      $ curl -X DELETE -u user:pass https://goo.ncc.unesp.br/api/v1/auth/1/

  .. sourcecode:: http

      DELETE /api/v1/auth/1/ HTTP/1.1
      Authorization: Basic dXNlcjpwYXNz
      User-Agent: curl/7.26.0
      Host: goo.ncc.unesp.br
      Accept: */*

  **Example response**:

  .. sourcecode:: http

      HTTP/1.0 204 NO CONTENT
      Content-Type: text/html; charset=utf-8

  :statuscode 204: No Content (Removed with success)
  :statuscode 401: Unauthorized
  :statuscode 404: Not found
