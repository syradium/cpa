from django.contrib.postgres.fields import JSONField
from django.db import models


class Order(models.Model):
    created_on = models.DateTimeField()
    order_id = models.IntegerField()
    domain = models.CharField(max_length=256)
    price = models.FloatField()
    utm_source = models.CharField(max_length=256, blank=True)
    utm_campaign = models.CharField(max_length=256, blank=True)
    utm_content = models.CharField(max_length=256, blank=True)
    data = JSONField(default=dict)
