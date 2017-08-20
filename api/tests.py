from django.test import TestCase
from streetart.models import Artwork, Artist, Artwork_Category

class ModelTestCase(TestCase):
    """This class defines the test suite for the streetart api."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.artwork = Artwork()
        self.artist = Artist(name="Test Artist", artist_from="Christchurch")
        self.category = Artwork_Category(name="Test Category")
        self.artist.save()
        self.category.save()

        self.artwork.name = "Write world class code"
        self.artwork.commission_date = "2017-08-01"
        self.artwork.longitude = "172.643366"
        self.artwork.latitude = "-43.531269"
        self.artwork.artist = self.artist
        self.artwork.category = self.category
        self.artwork.status = "Test"
        self.artwork.description = "Test"
        self.artwork.image = "Test"
        self.artwork.photo_credit = "Test"
        self.artwork.thumbnail = "Test"
        self.artwork.city = "Christchurch"

    def test_model_can_add_artwork(self):
        """Test the streetart model can rename an artwork."""
        old_count = Artwork.objects.count()
        self.artwork.save()
        new_count = Artwork.objects.count()
        self.assertNotEqual(old_count, new_count)