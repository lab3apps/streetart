# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-17 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0024_auto_20170917_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='twitter',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]