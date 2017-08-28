from django.contrib import admin
from .models import Artwork
from .models import Artist
from .models import Crew
from .models import Artwork_Category
from .models import Profile
from .models import Status
from .models import AlternativeImage
from mapwidgets.widgets import GooglePointFieldWidget
from django import forms
from django.contrib.gis.db import models


class ImageAdmin(admin.TabularInline):
    model = AlternativeImage

class ArtworkForm(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    filter_horizontal = ('artists',)
    inlines = [ ImageAdmin ]


admin.site.register(Artwork, ArtworkForm)
admin.site.register(Artist)
admin.site.register(Crew)
admin.site.register(Artwork_Category)
admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(AlternativeImage)
# Register your models here.
