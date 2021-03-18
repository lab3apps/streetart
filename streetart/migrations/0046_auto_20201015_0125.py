# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-14 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0045_featuredvideo_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredvideo',
            name='thumbnail_image',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='video_tumbnails/'),
        ),
        migrations.AlterField(
            model_name='featuredvideo',
            name='video_url',
            field=models.URLField(default='https://youtu.be/8313QiSmK8Q?t=3', verbose_name='Video URL'),
            preserve_default=False,
        ),
    ]