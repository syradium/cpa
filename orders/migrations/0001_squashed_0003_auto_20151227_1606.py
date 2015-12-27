# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 19:51
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
import django.contrib.postgres.operations
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('orders', '0001_initial'), ('orders', '0002_auto_20151227_1548'), ('orders', '0003_auto_20151227_1606')]

    initial = True

    dependencies = [
    ]

    operations = [
        django.contrib.postgres.operations.HStoreExtension(
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField()),
                ('domain', models.CharField(max_length=256)),
                ('price', models.FloatField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
