.. goo-server api documentation master file, created by
   sphinx-quickstart on Wed Dec 19 10:15:12 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to developer' corner!
=============================

The *Goo Server API* is a programmatic interface into many of the goo-server's
features. With this API you can make REST requests in a simple and transparent
way.

**Goo** is a multi component free and open-source project, you are visiting
now the *goo-server API documentation*. If you want to learn more about the Goo
Architecture, please refers to *Goo Architecture Documentation*.

To use the *Goo Server API* you must have a **GridUnesp account**. The API follows
the existing Users and Permissions system, so a user can only perform the operations
and actions on objects that they have permissions. You can submmit a job, cancel
a job, get a jobs status, upload and download objects and more.

If you have any questions about the API, please send an email to
goo@ncc.unesp.br.


Getting started
---------------

Authentication
^^^^^^^^^^^^^^

All requests require an API token, with one exception: ``api.v1.auth`` that can be
used to acquire or generate a user's API token through the API itself. To get
this token the User must inform their credentials.

You can pass your credentials using HTTP Basic Authentication:

.. sourcecode:: http

    https://user:pass@goo.ncc.unesp.br/api/v1/

And when you already have one token, use the API by sending a token request
parameter:

.. sourcecode:: http
    
    https://goo.ncc.unesp.br/api/v1/?token=946a0201-2dc4-46d0-9b6a-d12707abde78

.. note::

    ALWAYS use https connection.

Response Format
^^^^^^^^^^^^^^^

The optional parameter format can be set to either "json" or "xml". The default
is to output responses in JSON format.

JSON, or JavaScript Object Notation, is a simple, efficient, and easy to use
data object serialization method supported in many languages.

Extensible Markup Language (XML) is a markup language that defines a set of
rules for encoding documents in a format that is both human-readable and
machine-readable.

.. sourcecode:: http

    https://goo.ncc.unesp.br/api/v1/apps/?token=946a0201-2dc4-46d0-9b6a-d12707abde78&format=xml

.. toctree::
   :titlesonly:
   :maxdepth: 3
   :hidden:

   auth/get.auth.rst
   auth/get.auth.id.rst
   auth/get.auth.schema.rst
   auth/get.auth.set.id.id.rst
   auth/post.auth.rst
   auth/delete.auth.rst
   auth/delete.auth.id.rst

   token/get.token.rst

   apps/get.apps.rst
   apps/get.apps.id.rst
   apps/get.apps.schema.rst
   apps/get.apps.set.id.id.rst

   jobs/get.jobs.rst
   jobs/get.jobs.id.rst
   jobs/get.jobs.schema.rst
   jobs/get.jobs.set.id.id.rst
   jobs/post.jobs.rst
   jobs/delete.jobs.rst
   jobs/delete.jobs.id.rst

