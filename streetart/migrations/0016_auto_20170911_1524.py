# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-11 03:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0015_auto_20170911_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='artist_from',
            field=models.CharField(choices=[('green', 'green'), ('red', 'red')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='instagram',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
