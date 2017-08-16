# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-14 04:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0004_auto_20170814_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artwork_category',
            name='question',
        ),
        migrations.AlterField(
            model_name='crew',
            name='disband_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date disbanded'),
        ),
    ]