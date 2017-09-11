# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-11 04:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def artistfrom_text_to_relation(apps, schema_editor):
    """
    Changes the text field to a new artist_from.
    """
    artist_from_objs = {}
    Artist = apps.get_model('streetart', 'Artist')
    ArtistFrom = apps.get_model('streetart', 'ArtistFrom')

    for artist in Artist.objects.all():
        if artist.artist_from in artist_from_objs:
            _location = artist_from_objs[artist.artist_from]
        else:
            _location = ArtistFrom.objects.create()
            _location.location = artist.artist_from
            artist_from_objs[artist.artist_from] = _location
            _location.save()
        artist.artist_from_location = _location
        artist.save()

class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0019_auto_20170911_1615'),
    ]
    operations = [
        migrations.AddField(
            model_name='artist',
            name='artist_from_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='streetart.ArtistFrom'),
        ),
        migrations.RunPython(artistfrom_text_to_relation),
        migrations.RemoveField(
            model_name='artist',
            name='artist_from',
        ),
        migrations.AlterField(
            model_name='artwork',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='streetart.Artwork_Category'),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='streetart.Status'),
        ),
    ]