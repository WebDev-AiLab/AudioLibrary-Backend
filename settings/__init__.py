from .base import *
from .celery import *
from .path import *
from .cache import *
from .auth import *
from .mail import *
from .tinymce import *
from .ckeditor import *
from .api import *

# quick workaround to get rid of stupid errors
import django
from django.utils.encoding import force_str
from django.utils.translation import gettext

django.utils.encoding.force_text = force_str
django.utils.translation.ugettext = gettext
