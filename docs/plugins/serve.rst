Serve Plugin
============

The ``serve`` plugin is an ongoing effort to add a JSON/REST API to beets. It
is meant to be rather generic and usable from a HTML web application or any
other client.  

The ``serve`` does not provide any user interface. It only exposes expose the 
machine-readable API. Front-end will be provided either as separate plugins
or simply outside beets.

Install
-------

The Web interface depends on `Flask`_ and `Flask-restfull`_. To get these, just
 run ``pip install flask`` and ``pip install flask-restfull``.

.. _Flask: http://flask.pocoo.org/
.. _Flask-restfull: https://github.com/twilio/flask-restful

Put ``serve`` on your ``plugins`` line in your configuration file to enable the
plugin.

Run the Server
--------------

Then just type ``beet serve`` to start the server and go to
http://localhost:8337/. 

You can also specify the hostname and port number used by the Web server. These
can be specified on the command line or in the ``[serve]`` section of your
:doc:`configuration file </reference/config>`.

On the command line, use ``beet serve [HOSTNAME] [PORT]``. In the config file, 
use something like this::

    serve:
        host: 127.0.0.1
        port: 8888


JSON API General Principles
---------------------------

The API is modelled after the template of [JSONAPI](www.jsonapi.org).
Responses and requests bodies are json-formatted documents.

**Http Methods**

You should the appropriate HTTP method but if your client library does not 
support all methods, you can also use the ``X-HTTP-Method-Override`` Header.

**Filtering, searching and sorting** 

**Pagination**

**Discovery and HATEOS**


JSON API Endpoints
------------------


``GET /``
+++++++++

The root resource should only contains links to other resources.


``GET /items/``
+++++++++++++++



``GET /albums/``
++++++++++++++++



``GET /plugins/``
+++++++++++++++++

Could be used to discover the list of plugins that exposes actions through the REST API.

 

``GET /stats/``
+++++++++++++++

