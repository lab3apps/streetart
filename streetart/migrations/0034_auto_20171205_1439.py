# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-05 01:39
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0033_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media_thumbs/', verbose_name='Thumbnail'),
        ),
        migrations.AddField(
            model_name='media',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='If the video is not YouTube or Vimeo'),
        ),
        migrations.AlterField(
            model_name='media',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name="YouTube and Vimeo URL's supported"),
        ),
    ]
