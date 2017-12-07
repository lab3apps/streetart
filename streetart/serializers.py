from rest_framework import serializers
from streetart.models import Artwork, Artist, Artwork_Category, Route, RoutePoint, Crew, Artwork_Category, Status, User
from streetart.processors import add_watermark
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.core.serializers import serialize
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
import socket


#class ThumbnailSerializer(serializers.ImageField):
 #   def to_representation(self, instance):
 #       return thumbnail_url(instance, '420x250')


class ImageField(serializers.RelatedField):
    def to_representation(self, value):
        image = value.url

        #TODO: Add watermarking operations here
        #add_watermark(image_url, watermark_url)
        return image

class CrewSerializer(serializers.ModelSerializer):
    """Serializer to map the Crew instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Crew
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    """Serializer to map the Artist instance into JSON format."""
    crews = CrewSerializer(many=True, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Artist
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """Serializer to map the Category instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Artwork_Category
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    """Serializer to map the Status instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Status
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the Status instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

##class CommentSerializer(serializers.ModelSerializer):
##    """Serializer to map the Status instance into JSON format."""
##    user = UserSerializer(many=False, read_only=True)
##
##    class Meta:
##        """Meta class to map serializer's fields with the model fields."""
##        model = Comment
##        fields = ('id', 'object_pk', 'comment', 'ip_address', 'user', 'submit_date',)

class ArtworkSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    image = ImageField(source='watermarked_image', read_only=True)
    artists = ArtistSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    status = StatusSerializer(many=False, read_only=True)
    ##comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    checkins = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Artwork
        fields = ('id', 'image', 'thumbnail', 'photo_credit', 'artists', 'category', 'status', 'likes', 'checkins', 'title', 'commission_date', 'decommission_date', 'description', 'location', 'street', 'crews')

    def get_likes(self, obj):
        return obj.likes.count()

    def get_checkins(self, obj):
        return obj.checkins.count()

    def get_thumbnail(self, obj):

        if obj.cropped_image:
            #return obj.cropped_image.url
            return thumbnail_url(obj.cropped_image, 'cropped')
        else:
            #return obj.image.url
            return thumbnail_url(obj.image, 'uncropped')
class RouteArtworkSerializer(GeoFeatureModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Artwork
        geo_field = "location"
        fields = ('id', 'title','location')

class RoutePointSerializer(serializers.ModelSerializer):
    """Serializer to map the RoutePoint instance into JSON format."""
    artwork = RouteArtworkSerializer(many=False, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = RoutePoint
        fields = '__all__'

class RouteSerializer(GeoFeatureModelSerializer):
    """Serializer to map the Route instance into JSON format."""
    route_points = RoutePointSerializer(many=True, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Route
        geo_field = "route_points"
        fields = '__all__'