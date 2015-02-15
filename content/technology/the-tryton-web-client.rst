The Tryton Web Client
=====================

:date: 2012-03-12 00:00
:slug: tryton-web-client
:tags: tryton, python, web

The subject has been a topic of immense interest since 2008, and some even
believe that Tryton would have had a wider acceptance if it had a web client.
And with a lot of sarcasm Stefan Rijnhart tweeted a few days back:

.. image:: /images/content/technology/tweet-by-therp-stephan-tryton-web-client.png

Thanks to the motivation by Stefan, I finally decided to dedicate my weekend
to learning ExtJS (a wonderful JS framework I had wanted to play with since
its version 2) and to try and build a proof of concept for the Tryton web
client. From my previous conversations with Cedric and prior experiences 
a.k.a disasters with the OpenERP web client, I had set my goals for the 
project:

1. Should be similar to the GTK client in look, feel and functionality.
2. Must be a JS client side application and the server side should only be the 
   JSON RPC service of trytond.
3. It is a client for an ERP system, so should have the feel of a desktop
   application and not a social network or a blog.
4. Should work on tablets too (a picture from the ipad is attached).

So here is the result:

* The source code: https://github.com/openlabs/trytonweb
* A hosted link: http://openlabs.co.in/~st/trytonweb
* WSGI script to run your tryton: https://gist.github.com/2019037

So what does it include ?

* The client behaves exactly like a desktop app, so you can connect to
  remote/local tryton.
* Uses HTML5 localstorage to save the connection profiles
* A custom data handling proxy to easily use Tryton models

.. code-block:: javascript

    var ir_ui_menu_proxy = new Ext.createByAlias('proxy.tmodel', {
        modelName: "ir.ui.menu"
    });

    ir_ui_menu_proxy.doRequest(
        'search_read', 
        [['parent', '=', false], 0, 1000, null, ['name', 'childs']],

        // Callback
        function(result) {
          console.log(result);
        });

What does the WSGI script do ?

The script is the same as the one in the proposal by Cedric in 
`Issue 92001 <http://codereview.tryton.org/92001/>`_
except that it adds a Middleware to handle OPTIONS requests and CORS headers.

Some screenshots:

On the ipad
-----------

.. image:: /images/content/technology/tryton-web-client-1.png
    :alt: Tryton Web Client On the ipad

The login screen
----------------

.. image:: /images/content/technology/tryton-web-client-2.png
    :alt: Tryton Web Client The login Screen

Profile Editor
----------------

.. image:: /images/content/technology/tryton-web-client-3.png
    :alt: Profile editor of Tryton Web Client

Test with a bad password
------------------------

.. image:: /images/content/technology/tryton-web-client-4.png
    :alt: Test with a bad password on Tryton Web Client 

Successful login
----------------

.. image:: /images/content/technology/tryton-web-client-5.png
    :alt: After a successful login on Tryton Web Client


That is all for now.

Catch me on #tryton freenode IRC channel if you have questions.
