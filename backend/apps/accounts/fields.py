import os
from io import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from apps.attachments.utils import get_default_filename

try:
    from PIL import Image
except ImportError:
    import Image


def _profile_avtar_filename(filename):
    return "profile_pictures/{}".format(get_default_filename(filename))


class Config:
    width = 100
    height = 100

    upload_to = _profile_avtar_filename
    save_format = 'png'
    save_quality = 90

    select_area_width = 400
    select_area_height = 250

    default_avatar_image = "profile_pictures/default.png"


conf = Config()


class AvatarField(models.ImageField):
    def __init__(self, *args, **kwargs):
        self.width = kwargs.pop('width', conf.width)
        self.height = kwargs.pop('height', conf.height)
        kwargs['upload_to'] = kwargs.get('upload_to', conf.upload_to)

        super(AvatarField, self).__init__(*args, **kwargs)

    def save_form_data(self, instance, data):
        # if data and self.width and self.height:
        file_ = data['file']
        if file_:
            image = Image.open(StringIO(file_.read()))
            image = image.crop(data['box'])
            image = image.resize((self.width, self.height), Image.ANTIALIAS)

            content = StringIO()
            image.save(content, conf.save_format, quality=conf.save_quality)

            file_name = u'{}.{}'.format(os.path.splitext(file_.name)[0], conf.save_format)

            # new_data = SimpleUploadedFile(file.name, content.getvalue(), content_type='image/' + config.save_format)
            new_data = InMemoryUploadedFile(content, None, file_name, 'profile-avatars/' + conf.save_format,
                                            len(content.getvalue()), None)
            super(AvatarField, self).save_form_data(instance, new_data)

