from django.contrib.postgres.fields import JSONField
from django.db import models


class Order(models.Model):
    created_on = models.DateTimeField()
    order_id = models.IntegerField()
    domain = models.CharField(max_length=256)
    price = models.FloatField()
    data = JSONField(default=dict)