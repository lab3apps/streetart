# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-18 04:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0025_auto_20170917_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='artwork/')),
                ('link', models.URLField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]