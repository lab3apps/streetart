from rest_framework import serializers
from streetart.models import Artwork, Artist, Artwork_Category

class ArtworkSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Artwork
        fields = ('id', 'name')
        read_only_fields = ()