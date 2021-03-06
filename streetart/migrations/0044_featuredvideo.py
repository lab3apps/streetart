# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-14 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0043_remove_artwork_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='Video URL')),
                ('thumbnail_image', models.ImageField(max_length=500, upload_to='video_tumbnails/')),
            ],
        ),
    ]
