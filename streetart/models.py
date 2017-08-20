from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime

@python_2_unicode_compatible  # only if you need to support Python 2
class Crew(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    is_disbanded = models.BooleanField()
    formed_date = models.DateTimeField('date formed')
    disband_date = models.DateTimeField('date disbanded', blank=True, null=True)
    def __str__(self):
        return self.name

@python_2_unicode_compatible  # only if you need to support Python 2
class Artist(models.Model):
    crews = models.ManyToManyField(Crew)
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    artist_from = models.CharField(max_length=200)
    other_links = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

@python_2_unicode_compatible  # only if you need to support Python 2
class Artwork_Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

@python_2_unicode_compatible  # only if you need to support Python 2
class Artwork(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Artwork_Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    commission_date = models.DateTimeField('date commissioned')
    status = models.CharField(max_length=200, null=True)
    decommission_date = models.DateTimeField('date decommissioned', blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='artwork/', height_field=None, width_field=None, max_length=100)
    photo_credit = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='artwork_thumbnails/', height_field=None, width_field=None, max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    city = models.CharField(max_length=200)
    link = models.URLField()
    def __str__(self):
        return self.name










