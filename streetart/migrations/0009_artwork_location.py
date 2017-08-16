# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-16 10:13
from __future__ import unicode_literals

import django.contrib.gis.geos.point
from django.db import migrations
import location_field.models.spatial


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0008_auto_20170816_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='location',
            field=location_field.models.spatial.LocationField(default=django.contrib.gis.geos.point.Point(1.0, 1.0), srid=4326),
        ),
    ]