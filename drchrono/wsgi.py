"""
WSGI config for drchrono project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

project_path = '/home/ubuntu/DrChrono/BirthdayReminder'
if project_path not in sys.path:
	sys.path.append(project_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drchrono.settings")

application = get_wsgi_application()
