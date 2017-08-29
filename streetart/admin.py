from django.contrib import admin
from .models import Artwork, Artist, Crew, Artwork_Category, Profile, Status, AlternativeImage, ArtistExpressionOfInterest, WallSpace, MuralCommission
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
    list_display = ('title', 'validated', 'status')
    inlines = [ ImageAdmin ]


admin.site.register(Artwork, ArtworkForm)
admin.site.register(Artist)
admin.site.register(Crew)
admin.site.register(Artwork_Category)
admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(AlternativeImage)
admin.site.register(ArtistExpressionOfInterest)
admin.site.register(WallSpace)
admin.site.register(MuralCommission)
# Register your models here.
