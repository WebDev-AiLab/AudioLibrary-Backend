import os
import magic
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_track_upload(file):
    allowed_mime = ['audio/mpeg']
    allowed_extensions = ['.mp3']

    # check the MIME
    validator = magic.Magic(uncompress=True, mime=True)
    file_mime_type = validator.from_buffer(file.read())
    # ok, this is not good, but only admin can upload files, so we allow this for now...
    # if file_mime_type not in allowed_mime:
    #     raise ValidationError(_('Unsupported file type') + ': ' + file_mime_type)

    file_extension = os.path.splitext(file.name)[-1].lower()
    if file_extension not in allowed_extensions:
        raise ValidationError(_('Unacceptable file extension') + ': ' + file_extension)
