# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-13 14:18
from __future__ import unicode_literals

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0041_auto_20201014_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name="YouTube and Vimeo URL's supported"),
        ),
    ]
