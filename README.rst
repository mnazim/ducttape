========
ducttape
========

NIH utility for generating static html pages from a bunch of Django templates
without need to setup a full Django project.

I created it to help me prototype my web apps using Django Template Language.

Needs a unix like environment. I don't know what will happen to it on MS Windows.

Installation
============

Install using `pip`
::

    pip install git+https://github.com/mnazim/ducttape.git

Quick Start
===========

Follow the commands::

    $ mkdir ducttape-demo
    $ cd ducttape-demo
    $ ducttape init
    Initializing...
    Done

``init`` creates directory structure::

    (ducttape)$ ls
    context  output  static  templates

Template files go in ``templates`` directory, context data for templates goes
inside ``context`` directory(e.g, ``context/users/profile.json`` is the
context for ``templates/users/profile.html``). Generated html files are stored
``output`` directory. ``static`` directory is for js, css, images, etc.

If you have a ``context/global.json`` file, it will be available as context for
all templates. Values from ``global.json`` can be overridden from per template
contexts.

STATIC_URL, set to ``/static/`` and MEDIA_URL, set to ``/static/media/`` are
available inside templates automatically.


``watch`` monitors template files for changes and automatically rebuilds site as
needed::

    $ ducttape watch
    Watching...
    Building...
        article.html -> output/article.html
        index.html -> output/index.html
        users/mirnazim.html -> output/users/mirnazim.html
        users/index.html -> output/users/index.html
    Done


``export`` exports the generated output to a zipfile named ``output.zip``::

    $ ducttape export
    Building...
        article.html -> output/article.html
        index.html -> output/index.html
        users/mirnazim.html -> output/users/mirnazim.html
        users/index.html -> output/users/index.html
    Done
    Creating zip archive...
    Done

That's it. No configuration; only convention(for now, at least). Wait...

Yes, to serve the generated html files just use the SimpleHTTPServer::

    $ cd output
    $ python -m SimpleHTTPServer

Or for Python3::

    $ python3 -m http.serve
