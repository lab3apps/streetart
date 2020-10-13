# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-13 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0037_auto_20180627_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistexpressionofinterest',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artwork',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Video URL'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='muralcommission',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wallspace',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
