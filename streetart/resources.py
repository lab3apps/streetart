from import_export import resources
from .models import *

class ArtistResource(resources.ModelResource):
    class Meta:
        model = Artist

class ArtworkResource(resources.ModelResource):
    class Meta:
        model = Artwork

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
