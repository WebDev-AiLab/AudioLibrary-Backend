import os
from django.utils.deconstruct import deconstructible
from tools.string import generate_random_string


@deconstructible
class ModifyUpload(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f"{generate_random_string()}.{ext}"
        if instance.id:
            filename = f"{instance.id}_{filename}"
        return os.path.join('', self.path, filename)


process_filename = ModifyUpload('music')
