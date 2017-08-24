from rest_framework import serializers
from streetart.models import Artwork, Artist, Artwork_Category
from streetart.processors import add_watermark
import socket


class ImageField(serializers.RelatedField):
    def to_representation(self, value):
        image = value.url

        #TODO: Add watermarking operations here
        #add_watermark(image_url, watermark_url)
        return image

class ArtworkSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    image = ImageField(read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Artwork
        fields = ('id', 'title', 'artists', 'crew', 'category', 'description', 'commission_date', 'status_id', 'decommission_date', 'image', 'photo_credit', 'city', 'link', 'location', 'objects')
        read_only_fields = fields

class ArtistSerializer(serializers.ModelSerializer):
    """Serializer to map the Artist instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Artist
        fields = ('id', 'name', 'crews', 'website', 'facebook', 'instagram', 'twitter', 'artist_from', 'other_links')
        read_only_fields = fields
