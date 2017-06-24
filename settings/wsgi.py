"""
WSGI config for fairblogs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))
sys.path.insert(0, os.path.abspath(os.path.join(root_path)))
# sys.path.insert(0, os.path.abspath('/srv/fairblogs/venv/lib/python3.6/site-packages/'))
sys.path.insert(0, os.path.abspath('/srv/fairblogs/venv/lib/python2.7/site-packages/'))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
