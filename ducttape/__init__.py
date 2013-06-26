#!/usr/bin/env python
# -+- coding: utf-8 -*-

"""
NIH utility for generating static html pages from a bunch of Django templates
without need to setup a full Django project.(README.rst)

:copyright: (C) 2013 Mir Nazim <hi@mirnazim.org>
:license: MIT License (See LICENSE.txt for details)

Usage:
    $ ducttape.py init <path/to/project>
    $ cd <project>
    $ ducttape.py watch
"""

import os
import sys
import subprocess
import datetime
import time
import zipfile
import argparse
import json

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from django.conf import settings as django_settings
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from django.template.loader import render_to_string

__version__ = '0.1a1'

SETTINGS = {
    'engine': 'django',
    'template_dir': 'templates',
    'context_dir': 'context',
    'static_dir': 'static',
    'output_dir': 'output',
}
GLOBAL_CONTEXT = {
    'STATIC_URL': '/static/',
    'MEDIA_URL': '/static/media/',
}


django_settings.configure(
    DEBUG = True,
    TEMPLATE_DEBUG = True,
    TEMPLATE_DIRS = (SETTINGS['template_dir'],),
)

def _load_settings():
    global SETTINGS
    return SETTINGS


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, site):
        super(ChangeHandler, self).__init__()
        self.site = site
        self.site.build()

    def on_any_event(self, event):
        src_file = event._src_path[len(os.path.abspath(self.site.settings.get('template_dir'))) + 1:]
        print "[{event_type}] {src}".format(src=src_file, event_type=event.event_type)
        self.site.build()

class Page(object):
    def __init__(self, dirname, filename, ext):
        settings = _load_settings()
        self.dirname = dirname
        self.filename = filename
        self.ext = ext
        self.template_path = os.path.join(self.dirname, self.filename + self.ext)
        self.context_path = os.path.join(settings.get('context_dir', 'context'), self.dirname, self.filename + '.json')
        self.output_path = os.path.join(settings.get('output_dir', 'output'), self.dirname, self.filename + self.ext)
        self.context = self._get_context()

    def _get_context(self):
        global GLOBAL_CONTEXT
        context = {}
        try:
            if os.path.exists(self.context_path) and os.path.isfile(self.context_path):
                _c = open(self.context_path).read()
                if _c.strip():
                    context = json.loads(_c)
                    context.update(GLOBAL_CONTEXT)
        except ValueError:
            print("{file} does not contain valid json".format(file=self.context_path))

        return context


    def __repr__(self):
        return self.template_path

    def build(self):
        print "    {src} -> {out}".format(src=self.template_path, out=self.output_path)
        html = render_to_string(self.template_path, self.context)
        try:
            os.makedirs(os.path.dirname(self.output_path))
        except OSError:
            pass

        with open(self.output_path, 'w') as f:
            f.write(html)


class Site(object):
    """The main site object, where everything is assembled"""

    def __init__(self, settings):
        self.settings = settings
        self.pages = []

    def _collect_pages(self):
        self.pages = []
        template_dir = self.settings.get('template_dir', 'templates')
        if not template_dir.endswith('/'):
            template_dir = template_dir + '/'

        for root, dirs, files in os.walk(template_dir):
            for f in files:
                if f.startswith('_'):
                    continue

                dirname = os.path.dirname(os.path.join(root, f))
                dirname = dirname[len(template_dir): ]
                filename, ext = os.path.splitext(f)
                self.pages.append(Page(dirname, filename, ext))

    def build(self):
        self._collect_pages()
        print "Building..."
        for page in self.pages:
            page.build()
        self.add_static()
        print "Done"

    def add_static(self):
        dest = os.path.abspath(os.path.join(self.settings.get('output_dir'), self.settings.get('static_dir')))
        src = os.path.abspath(self.settings.get('static_dir'))
        if os.path.lexists(dest):
            os.unlink(dest)
        os.symlink(src, dest)

    def init(self):
        if len(os.listdir('.')) > 0:
            print "Cannot initialize. This directory is not empty."
            sys.exit()
        print "Initializing..."
        os.makedirs(self.settings.get('template_dir'))
        os.makedirs(self.settings.get('context_dir'))
        os.makedirs(self.settings.get('output_dir'))
        os.makedirs(os.path.join(self.settings.get('static_dir'), 'media'))
        self.add_static()
        print "Done"

    def watch(self):
        print 'watching...'
        event_handler = ChangeHandler(self)
        observer = Observer()
        observer.schedule(event_handler, os.path.abspath('templates'), recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def export(self):
        self.build()
        zip = zipfile.ZipFile("output.zip", "w")
        print "Creating zip archive..."
        for page in self.pages:
            zip.write(page.output_path)
        zip.close()
        print "Done"


def _usage():
    print """Usage:
    ducttape init    (Initialize the project)
    ducttape watch   (Watch templates for changes and auto-rebuild)
    ducttape export  (Export generated html to a zip file)
    """

def main():
    site = Site(_load_settings())
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('action', action="store", default=True,
                        help="init|watch|export")
    parser.print_help = _usage
    args = parser.parse_args()
    if args.action == 'init':
        site.init()
    elif args.action == 'watch':
        site.watch()
    elif args.action == 'export':
        site.export()
    else:
        print
        print "Action must be one of the :",
        print "init, watch, export"
        print "I don't know what to do with '{action}'".format(action=args.action)


if __name__ == '__main__':
    main()
