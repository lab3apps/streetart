# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-17 00:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0009_artwork_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artwork',
            name='location',
        ),
    ]