# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-15 22:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0029_auto_20171009_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='watermarked_image',
            field=models.ImageField(max_length=500, null=True, upload_to='API_artwork/'),
        ),
    ]
