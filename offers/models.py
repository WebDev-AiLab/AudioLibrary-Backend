from django.db import models
from tracks.models import Submission
from tools.basemodels import GenericIDModel


class Offer(Submission):
    class Meta:
        proxy = True


class OfferLink(GenericIDModel):
    link = models.CharField(max_length=2048)

    SOURCE_CHOICES = (
        ('youtube', 'YouTube'),
    )
    source = models.CharField(max_length=64, choices=SOURCE_CHOICES, null=True, blank=True, db_index=True)
    title = models.CharField(max_length=2048, null=True, blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
