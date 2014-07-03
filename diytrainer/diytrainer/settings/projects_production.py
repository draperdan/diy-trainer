"""Production settings and globals."""

""" For app served to projects.diy-trainer.com """

from __future__ import absolute_import

from os import environ

from .production import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

SITE_ID = 2

ROOT_URLCONF = 'projects_urls.py'
