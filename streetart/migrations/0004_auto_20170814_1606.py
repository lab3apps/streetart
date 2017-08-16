# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-14 04:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streetart', '0003_remove_artist_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='crews',
            field=models.ManyToManyField(blank=True, null=True, to='streetart.Crew'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='other_links',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='crew',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='streetart.Crew'),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='decommission_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date decommissioned'),
        ),
    ]