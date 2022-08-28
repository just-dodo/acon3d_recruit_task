from unicodedata import name
from django.db import models
from core.common_models import TimeModel
from django.contrib.auth.models import User


class Merchandise(TimeModel):
    name = models.CharField(max_length=500)
    author = models.ForeignKey(
        User, related_name="merchandises", on_delete=models.SET_NULL, null=True
    )
    released_at = models.DateTimeField(null=True,blank=True, default=None)
    is_submitted = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    #TODO
    #image, file

class MerchContent(TimeModel):
    merchendise = models.ForeignKey(
        Merchandise, related_name="contents", on_delete=models.CASCADE
    )

    LanguageChoices = (
        ("ko", "Korean"),
        ("en", "English"),
        ("zh", "Chinese"),
    )
    language = models.CharField(
        max_length=10, choices=LanguageChoices, default="Korean"
    )

    title = models.CharField(max_length=100)
    body = models.TextField(max_length=10000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
