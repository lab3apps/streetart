from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models
from sorl.thumbnail import ImageField
from django.template.defaultfilters import slugify
from fluent_comments.models import Comment
from django.contrib.contenttypes.models import ContentType

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
class Status(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

@python_2_unicode_compatible  # only if you need to support Python 2
class Artwork(models.Model):
    artists = models.ManyToManyField(Artist, blank=True,related_name='artworks')
    crews = models.ManyToManyField(Crew, blank=True, related_name='artworks')
    category = models.ForeignKey(Artwork_Category, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    commission_date = models.DateField('date commissioned', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)
    decommission_date = models.DateField('date decommissioned', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = ImageField(upload_to='artwork/')
    photo_credit = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    location = models.PointField(srid=4326)
    objects = models.GeoManager()
    validated = models.BooleanField(default=False)
    slug = models.SlugField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    checkins = models.ManyToManyField(User, related_name='checkins', blank=True)
    submitter_description = models.TextField(blank=True, null=True, verbose_name="Submitter's Description")
    submitter_name = models.CharField(blank=True, null=True, max_length=200, verbose_name="Submitter's Name")
    submitter_email = models.EmailField(blank=True, null=True, verbose_name="Submitter's Email Address")

    @property
    def total_likes(self):
        """
        Likes for the artwork
        :return: Integer: Likes for the artwork
        """
        return self.likes.count()

    @property
    def total_checkins(self):
        """
        Check ins for the artwork
        :return: Integer: Check ins for the artwork
        """
        return self.checkins.count()

    @property
    def comments(self):
        ct = ContentType.objects.get_for_model(Artwork)
        obj_pk = self.id
        return Comment.objects.filter(content_type=ct,object_pk=obj_pk)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Artwork, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

@python_2_unicode_compatible  # only if you need to support Python 2
class AlternativeImage(models.Model):
    image = ImageField(upload_to='artwork/')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='other_images')

@python_2_unicode_compatible  # only if you need to support Python 2
class MuralCommission(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    contact = models.TextField()
    def __str__(self):
        return self.title

@python_2_unicode_compatible  # only if you need to support Python 2
class WallSpace(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    contact = models.TextField()
    def __str__(self):
        return self.title

@python_2_unicode_compatible  # only if you need to support Python 2
class ArtistExpressionOfInterest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    contact = models.TextField()
    def __str__(self):
        return self.title

@python_2_unicode_compatible  # only if you need to support Python 2
class Route(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

@python_2_unicode_compatible  # only if you need to support Python 2
class RoutePoint(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_points')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='route_points')
    route_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('route_order',)

    @property
    def location(self):
        return self.artwork.location

    def __str__(self):
        return "" ##This is needed for the use of drag and drop sorting plugin in admin.






