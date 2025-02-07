from django.db import models

from lms.core.compat import get_user_model

UserModel = get_user_model()


class AuthorField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("to", UserModel)
        kwargs.setdefault("on_delete", models.CASCADE)
        super().__init__(*args, **kwargs)
