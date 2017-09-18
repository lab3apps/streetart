from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from multiselectfield import MultiSelectField
from easy_thumbnails.files import get_thumbnailer
from image_cropping import ImageRatioField
from image_cropping.utils import get_backend
from PIL import Image
from django_comments_xtd.moderation import moderator, XtdCommentModerator, SpamModerator
from streetart.badwords import badwords
from streetart.processors import convert_rgba

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
class ArtistFrom(models.Model):
    location = models.CharField(max_length=200)
    def __str__(self):
        return self.location

@python_2_unicode_compatible  # only if you need to support Python 2
class Artist(models.Model):
    crews = models.ManyToManyField(Crew, blank=True)
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    artist_from_location = models.ForeignKey(ArtistFrom, on_delete=models.SET_NULL, blank=True, null=True)
    artist_from = models.CharField(max_length=200, null=True)
    other_links = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
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
    category = models.ForeignKey(Artwork_Category, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    commission_date = models.CharField(max_length=200, blank=True, null=True, verbose_name='date commissioned')
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, blank=True, null=True)
    decommission_date = models.CharField(max_length=200, blank=True, null=True, verbose_name='date decommissioned')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='artwork/', max_length=500)
    cropping = ImageRatioField('image', '250x250')
    cropped_image = models.ImageField(upload_to='artwork/', blank=True, null=True, max_length=500)
    def image_thumbnail(self):
        thumbnailer = get_thumbnailer(self.image)
        thumbnail_options = {'size': (250, 250)}
        thumbnailer.get_thumbnail(thumbnail_options)
        return '<img src="%s" />' % thumbnailer.get_thumbnail(thumbnail_options).url
    image_thumbnail.short_description = 'Uploaded Image'
    image_thumbnail.allow_tags = True

    photo_credit = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    location = models.PointField(srid=4326)
    objects = models.GeoManager()
    validated = models.BooleanField(default=False)
    street = models.CharField(max_length=200, blank=True, null=True, verbose_name="What street is the artwork on (to help in identifying)")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Write any notes about the artwork here (will not be shown on map)")
    map_enabled = models.BooleanField(default=True, verbose_name="Show this artwork on the map")
    smart_cities = models.BooleanField(default=True,verbose_name="Allow this artwork to be accessed by smartcities")
    slug = models.SlugField(max_length=255, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    checkins = models.ManyToManyField(User, related_name='checkins', blank=True)
    submitter_description = models.TextField(blank=True, null=True, verbose_name="Submitter's Description")
    submitter_name = models.CharField(blank=True, null=True, max_length=200, verbose_name="Submitter's Name")
    submitter_email = models.EmailField(blank=True, null=True, verbose_name="Submitter's Email Address")

    def get_absolute_url(self):
        return "/artwork/%d" % self.id

    def get_artists(self):
        return "\n".join([p.name for p in self.artists.all()])

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
        if self.image != self.__original_image:
            self.image = convert_rgba(self.image)
        if self.pk and self.image == self.__original_image:
            self.cropped_image = get_thumbnailer(self.image).get_thumbnail(
                {
                    'size': (10000, 10000),
                    'box': self.cropping,
                    'crop': True,
                    'detail': True,
                }
            ).name
        if self.title != None and self.title != '':
            self.slug = slugify(self.title)
        else:
            self.slug = slugify(self.pk)
        super(Artwork, self).save(*args, **kwargs)

    def __str__(self):
        if self.pk and (self.title != "" or (self.artists.all().count() > 1 or (self.artists.all().count() == 1 and self.artists.filter(name="").count() != 1))):
            return_string = ""
            if self.title != "":
                return_string += self.title
            else:
                return_string += "Untitled"
            if self.artists.all().count() > 0:
                return_string += " by " + ", ".join([artist.__str__() for artist in self.artists.all()])
            if self.street and self.street != "":
                return_string += ", on " + self.street
            return  return_string
        else:
            return "Unknown Artwork" + ((", on " + self.street) if (self.street and self.street != "") else "")

    def __init__(self, *args, **kwargs):
        super(Artwork, self).__init__(*args, **kwargs)
        self.__original_image = self.image

@python_2_unicode_compatible  # only if you need to support Python 2
class AlternativeImage(models.Model):
    image = models.ImageField(upload_to='artwork/alternate/', max_length=500)
    def image_thumbnail(self):
        thumbnailer = get_thumbnailer(self.image)
        thumbnail_options = {'size': (250, 250)}
        thumbnailer.get_thumbnail(thumbnail_options)
        return '<img src="%s" />' % thumbnailer.get_thumbnail(thumbnail_options).url
    image_thumbnail.short_description = 'Uploaded Image'
    image_thumbnail.allow_tags = True
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='other_images')
    def save(self, *args, **kwargs):
        if self.image != self.__original_image:
            self.image = convert_rgba(self.image)
        super(AlternativeImage, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(AlternativeImage, self).__init__(*args, **kwargs)
        self.__original_image = self.image


@python_2_unicode_compatible  # only if you need to support Python 2
class MuralCommission(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=15)
    mural_location = models.PointField(srid=4326, verbose_name="Where will the mural be?")
    objects = models.GeoManager()
    dimensions = models.TextField(blank=True, null=True, verbose_name="How big is the wall? Please give us the dimensions of the wall so we can give the artist an idea of how big the space is.")
    image = models.ImageField(upload_to='muralcommission/', blank=True, null=True, verbose_name="If possible please attach a photo of the wall.", max_length=500)
    reason = models.TextField(blank=True, null=True, verbose_name="Most artists prefer to have creative freedom when creating their works, but could you give us an idea of what you are commissioning the mural for or what you hope to see in it? This will help us figure out which artists to get you in contact with.")
    budget = models.TextField(blank=True, null=True, verbose_name="Do you have a budget? Roughly how much have you put aside for the art work?")
    deadline = models.TextField(blank=True, null=True, verbose_name="Does this project have a deadline?")
    other = models.TextField(blank=True, null=True, verbose_name="Is there anything else we should know that will help us to connect you up with the right artist?")
    def __str__(self):
        return self.name

@python_2_unicode_compatible  # only if you need to support Python 2
class WallSpace(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=15)
    wall_location = models.PointField(srid=4326, verbose_name="Where is the space?")
    objects = models.GeoManager()
    dimensions = models.TextField(blank=True, null=True, verbose_name="How big is the wall? Please give us the dimensions of the wall so we can give the artist an idea of how big the space is.")
    image = models.ImageField(upload_to='wallspace/', blank=True, null=True, verbose_name="If possible please attach a photo of the wall.", max_length=500)
    relation = models.TextField(blank=True, null=True, verbose_name="What is your relation to this wall space?")
    other = models.TextField(blank=True, null=True, verbose_name="Is there anything else we should know?")
    def __str__(self):
        return self.name

PROJECT_TYPE_CHOICES = ((1, 'Paid commisionings'),
               (2, 'I would consider unpaid opportunities or less than market rate. I am more interested in building my portfolio and giving back to the community.'),
               (3, 'Mentoring and teaching opportunties. Working with up and coming artists or students.'),)

@python_2_unicode_compatible  # only if you need to support Python 2
class ArtistExpressionOfInterest(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=15)
    project_types = MultiSelectField(choices=PROJECT_TYPE_CHOICES)
    location = models.TextField(blank=True, null=True, verbose_name="Are you located in Christchurch? If not, where are you from?")
    why = models.TextField(blank=True, null=True, verbose_name="Why do you want to create work here in Christchurch?")
    materials = models.TextField(blank=True, null=True, verbose_name="Would you be able to organize your own materials? What supplies do you require us to organize for you?")
    samples = models.TextField(blank=True, null=True, verbose_name="Please provide samples of past work or include a link to your website or portfolio.")
    other = models.TextField(blank=True, null=True, verbose_name="Is there anything you'd like us to know?")
    def __str__(self):
        return self.title

@python_2_unicode_compatible
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

@python_2_unicode_compatible  # only if you need to support Python 2
class GetInvolved(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='artwork/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

@python_2_unicode_compatible  # only if you need to support Python 2
class WhatsNew(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='artwork/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

@python_2_unicode_compatible  # only if you need to support Python 2
class Logo(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='logos/', blank=True, null=True, max_length=500)
    def image_thumbnail(self):
        if self.image:
            thumbnailer = get_thumbnailer(self.image)
            thumbnail_options = {'size': (250, 250)}
            thumbnailer.get_thumbnail(thumbnail_options)
            return '<img src="%s" />' % thumbnailer.get_thumbnail(thumbnail_options).url
    image_thumbnail.short_description = 'Uploaded Image'
    image_thumbnail.allow_tags = True
    link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if (self.image != self.__original_image) and self.image:
            self.image = convert_rgba(self.image)

        super(Logo, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super(Logo, self).__init__(*args, **kwargs)
        self.__original_image = self.image

class PostCommentModerator(SpamModerator):
    removal_suggestion_notification = True
    email_notification = True

    def moderate(self, comment, content_object, request):
        # Make a dictionary where the keys are the words of the message and
        # the values are their relative position in the message.
        def clean(word):
            ret = word
            if word.startswith('.') or word.startswith(','):
                ret = word[1:]
            if word.endswith('.') or word.endswith(','):
                ret = word[:-1]
            return ret

        lowcase_comment = comment.comment.lower()
        msg = dict([(clean(w), i)
                    for i, w in enumerate(lowcase_comment.split())])
        for badword in badwords:
            if isinstance(badword, str):
                if lowcase_comment.find(badword) > -1:
                    return True
            else:
                lastindex = -1
                for subword in badword:
                    if subword in msg:
                        if lastindex > -1:
                            if msg[subword] == (lastindex + 1):
                                lastindex = msg[subword]
                        else:
                            lastindex = msg[subword]
                    else:
                        break
                if msg.get(badword[-1]) and msg[badword[-1]] == lastindex:
                    return True
        return super(PostCommentModerator, self).moderate(comment,
                                                          content_object,
                                                          request)

moderator.register(Artwork, PostCommentModerator)

