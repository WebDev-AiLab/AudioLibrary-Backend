from django.db import models
from tools.basemodels import GenericUUIDModel


class Subscriber(GenericUUIDModel):
    email = models.EmailField(max_length=255, unique=True)
