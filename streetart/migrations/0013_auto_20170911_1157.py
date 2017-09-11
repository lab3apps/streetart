# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-10 23:57
from __future__ import unicode_literals

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0012_auto_20170911_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='cropped_image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='artwork/cropped'),
        ),
    ]
