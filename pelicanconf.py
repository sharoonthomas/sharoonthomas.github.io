#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Sharoon Thomas'
SITENAME = u'Outbox'
SITEURL = 'www.sharoonthomas.com'

THEME = "pelican-themes/pure-single"

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('github', 'https://github.com/sharoonthomas/'),
    ('linkedin', 'https://www.linkedin.com/in/sharoonthomas'),
    ('twitter-square', 'https://twitter.com/sharoonthomas'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Theme settings
PROFILE_IMG_URL = "images/gravatar.png"
COVER_IMG_URL = "images/light-in-a-bottle.jpg"

STATIC_PATHS = ['images']
READERS = {'html': None}
OUTPUT_RETENTION = ('CNAME',)
