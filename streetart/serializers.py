from rest_framework import serializers
from streetart.models import Artwork, Artist, Artwork_Category, Route, RoutePoint, Crew, Artwork_Category, Status, User
from fluent_comments.models import Comment
from streetart.processors import add_watermark
import socket



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

class CommentSerializer(serializers.ModelSerializer):
    """Serializer to map the Status instance into JSON format."""
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Comment
        fields = ('id', 'object_pk', 'comment', 'ip_address', 'user', 'submit_date',)

class ArtworkSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    image = ImageField(read_only=True)
    artists = ArtistSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    status = StatusSerializer(many=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    checkins = serializers.SerializerMethodField()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Artwork
        fields = '__all__'

    def get_likes(self, obj):
        return obj.likes.count()

    def get_checkins(self, obj):
        return obj.checkins.count()

class RoutePointSerializer(serializers.ModelSerializer):
    """Serializer to map the RoutePoint instance into JSON format."""
    artwork = ArtworkSerializer(many=False, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = RoutePoint
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    """Serializer to map the Route instance into JSON format."""
    route_points = RoutePointSerializer(many=True, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Route
        fields = '__all__'