Debugging the Tryton client on a mac
====================================

:date: 2015-07-20
:slug: debugging-tryton-client-on-mac
:tags: tryton, python, client, osx

.. image:: images/content/technology/iterm-tryton-log.png
   :alt: Tryton logs with highlighting

If you use a mac for Tryton development, you have two choices of using the
Tryton client:

  1. `Download <http://downloads.tryton.org/3.6/>`_ the pre-baked application
     from Tryton downloads.
  2. `Build the tryton client on a mac 
     <https://code.google.com/p/tryton/wiki/BuildingMacOSXInstall>`_. This
     is inevitable if you want to develop on the tryton client or fix a
     bug in it.

Why would I want to debug on Tryton client ?
--------------------------------------------

Three reasons:

  1. The development mode: By launching the tryton client in development
     mode (``-d``), you can ask Tryton client not to cache the views and
     fetch it every time from the server. Comes in very handy when you are
     iteratively building your views.
  2. The verbose mode: The Tryton client will start logging a bit more 
     at the INFO level and also show stack traces. Include ``-v`` as an option.
  3. Debugging RPC calls: If you want to see how the Tryton client
     communicates with the server, logging at the DEBUG level (``-l DEBUG``)
     will spit out all requests and responses.

When using prebaked application
-------------------------------

When using the pre-baked application, the arguments to the Tryton client
cannot be passed directly to the application bundle. The `open
command <https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/open.1.html>`_ 
usually used to open applications has a ``--arg`` option which lets you send
arguments to the underlying application runner.

.. code-block:: shell

   $ open -a /Applications/Tryton.app --args -v -d

.. tip::

    Pro Tip: If you already have a running Tryton client, but want to open 
    another instance, you can use the `-n` option.

But where are my logs ? Well, they get shipped straight to system logs.
You could either 

.. code-block:: shell

    $ tail /var/log/system.log

or view the logs on a GUI using the `console application 
<https://en.wikipedia.org/wiki/Console_(OS_X)>`_.

.. image:: images/content/technology/logs-from-tryton-client.png
   :alt: Screenshot of the console logs

For the brave of heart
----------------------

If you are brave enough to get GTK working on your mac, you can run the
tryton client like you would on a linux machine. Remember to install Gtk on
a different system user. If you ever decide to make a redistributable app, 
the packages you have installed using Homebrew and MacPorts will come haunting.

Here is what I do to get the Tryton client to run in the same window but
as a different user.

.. code-block:: shell

   $ sudo su gtkosxuser
   $ export PATH=/Users/gtkosxuser/.local/bin:/Users/gtkosxuser/gtk/inst/bin:$PATH
   $ cd tryton-3.4
   $ bin/tryton -d -v

Line 2 in the above example adds Gtk to the `PATH`.

Bonus: Highlighting of RPC logs
-------------------------------

At `Fulfil.IO <https://www.fulfil.io>`_ we build client applications like
POS and custom web clients for Tryton which communicate to the Tryton
server over RPC. Knowing what the Tryton client does over RPC comes in
very handy and the DEBUG logs are synchronous (mostly).

To make this easier, you could highlight the request and response to make
the logs easier to read. If you use `iTerm <https://www.iterm2.com/>`_
(which you should), you can set this up in ``Preferences > Profiles >
Advanced > Triggers``. Here is what my triggers look like:

.. image:: images/content/technology/iterm-tryton-log-triggers.png
    :alt: Tryton logs iterm preferences regex

And the logs would look like the first image on this post.

Happy developing!
