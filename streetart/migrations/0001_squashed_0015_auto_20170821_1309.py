# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-21 04:50
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    replaces = [('streetart', '0001_initial'), ('streetart', '0002_auto_20170810_1626'), ('streetart', '0003_remove_artist_question'), ('streetart', '0004_auto_20170814_1606'), ('streetart', '0005_auto_20170814_1610'), ('streetart', '0006_auto_20170814_1613'), ('streetart', '0007_profile'), ('streetart', '0008_auto_20170816_1719'), ('streetart', '0009_artwork_location'), ('streetart', '0010_remove_artwork_location'), ('streetart', '0011_artwork_location'), ('streetart', '0012_auto_20170817_1343'), ('streetart', '0013_auto_20170818_1152'), ('streetart', '0014_auto_20170818_1217'), ('streetart', '0015_auto_20170821_1309')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('website', models.URLField()),
                ('facebook', models.URLField()),
                ('instagram', models.URLField()),
                ('twitter', models.URLField()),
                ('artist_from', models.CharField(max_length=200)),
                ('other_links', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('commission_date', models.DateTimeField(verbose_name='date commissioned')),
                ('status', models.CharField(max_length=200)),
                ('decommission_date', models.DateTimeField(verbose_name='date decommissioned')),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='artwork/')),
                ('photo_credit', models.CharField(max_length=200)),
                ('thumbnail', models.ImageField(upload_to='artwork_thumbnails/')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('city', models.CharField(max_length=200)),
                ('link', models.URLField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streetart.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Artwork_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('is_disbanded', models.BooleanField()),
                ('formed_date', models.DateTimeField(verbose_name='date formed')),
                ('disband_date', models.DateTimeField(blank=True, null=True, verbose_name='date disbanded')),
            ],
        ),
        migrations.AddField(
            model_name='artwork',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='streetart.Artwork_Category'),
        ),
        migrations.AddField(
            model_name='artwork',
            name='crew',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='streetart.Crew'),
        ),
        migrations.AddField(
            model_name='artist',
            name='crews',
            field=models.ManyToManyField(to='streetart.Crew'),
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
            name='decommission_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date decommissioned'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='artwork',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
        migrations.RemoveField(
            model_name='artwork',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='artwork',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='artwork',
            name='thumbnail',
        ),
        migrations.AlterField(
            model_name='artwork',
            name='commission_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date commissioned'),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to='artwork/'),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='streetart.Artist'),
        ),
    ]