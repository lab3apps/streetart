from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models
from sorl.thumbnail import ImageField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.user.__str__()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

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
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Artwork_Category, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    commission_date = models.DateTimeField('date commissioned', blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    decommission_date = models.DateTimeField('date decommissioned', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = ImageField(upload_to='artwork/')
    photo_credit = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    location = models.PointField(srid=4326)
    objects = models.GeoManager()

    def __str__(self):
        return self.name










