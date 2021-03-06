# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-15 22:16
from __future__ import unicode_literals


import os
from django.db import migrations, models
from streetart.processors import add_watermark
from PIL import Image
from chch_streetart.settings import STATIC_ROOT


def migrate_watermarked_image(apps, schema_editor):
    artwork = apps.get_model("streetart", "artwork")
    for i in artwork.objects.all():
        i.watermarked_image = add_watermark(i.image, Image.open(os.path.join(STATIC_ROOT, 'img/wts-watermark-logo-white.png')))
        i.save()

class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0034_auto_20171205_1439'),
    ]

    operations = [
        migrations.RunPython(migrate_watermarked_image),
    ]
