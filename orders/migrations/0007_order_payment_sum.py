# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20160106_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_sum',
            field=models.IntegerField(default=0),
        ),
    ]