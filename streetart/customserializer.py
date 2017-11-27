from rest_framework import serializers
import logging
from .models import Artwork, Artist
from rest_framework.generics import GenericAPIView

logger = logging.getLogger('watch_this_space')

class cArtistSerializer(serializers.ModelSerializer):
    """Serializer to map the Artist instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Artist
        fields = ('name', "website", "facebook", "instagram", "twitter", "biography")


class ArtworksSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField('imageurl')
    lat = serializers.SerializerMethodField('lattitude')
    lng = serializers.SerializerMethodField('longitude')
    hasLiked = serializers.SerializerMethodField('HasLiked')
    likes_count = serializers.SerializerMethodField('LikesCount')
    hasCheckedin = serializers.SerializerMethodField('HasCheckedIn')
    checkins_count = serializers.SerializerMethodField('CheckInCounts')
    artists = cArtistSerializer(many=True, read_only=True)
    ##altImages = cAlterImageSerializer(many=True, read_only=True)
    altImages = serializers.SerializerMethodField('AlterImages')

    def imageurl(self, obj):
        return obj.image.url

    def lattitude(self, obj):
        return obj.location.y

    def longitude(self, obj):
        return obj.location.x

    def HasLiked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated():
            return obj.likes.filter(id=user.id).exists()
        else:
            return False

    def LikesCount(self, obj):
        return obj.total_likes

    def HasCheckedIn(self, obj):
        user = self.context['request'].user
        if user.is_authenticated():
            return obj.checkins.filter(id=user.id).exists()
        else:
            return False

    def CheckInCounts(self, obj):
        return obj.total_checkins

    def AlterImages(self, obj):
        list = []
        for img in obj.other_images.all():
            list.append(img.image.url)

        ret = ",".join(list)
        return ret

    class Meta:
        model = Artwork
        fields = ("pk","title", "description", "commission_date", "decommission_date", "status",
                  "photo_credit", "link", "imageUrl", "artists", "lat", "lng", "hasLiked",
                  "likes_count", "hasCheckedin", "checkins_count", "altImages")
