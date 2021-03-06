# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-05 00:36
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0032_auto_20171129_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video', embed_video.fields.EmbedVideoField(verbose_name="YouTube and Vimeo URL's supported")),
            ],
        ),
    ]
