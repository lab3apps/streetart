from django.contrib import admin
from .models import Artwork, Artist, Crew, Artwork_Category, Profile, Status, AlternativeImage, ArtistExpressionOfInterest, WallSpace, MuralCommission, Route, RoutePoint, Section, Logo
from mapwidgets.widgets import GooglePointFieldWidget
from django import forms
from django.contrib.gis.db import models
from adminsortable2.admin import SortableInlineAdminMixin
from image_cropping import ImageCroppingMixin


class ImageAdmin(admin.TabularInline):
    model = AlternativeImage
    readonly_fields = ('image_thumbnail',)

class ArtworkForm(ImageCroppingMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    exclude = ('likes', 'checkins', 'cropped_image')
    filter_horizontal = ('artists', 'crews')
    list_display = ('pk', 'image_thumbnail', 'title', 'get_artists', 'validated', 'status')
    inlines = [ ImageAdmin ]
    readonly_fields = ('image_thumbnail',)
    search_fields = ['title', 'artists__name', 'description']

class NewInfoForm(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

class ArtistForm(admin.ModelAdmin):
    search_fields = ('name',)

class RoutePointInline(SortableInlineAdminMixin, admin.TabularInline):
    model = RoutePoint

class RouteForm(admin.ModelAdmin):
    inlines = [ RoutePointInline ]
    class Media: 
        css = {
             'all': ('streetart/css/admin/route_admin.css',)
        }

class LogoForm(admin.ModelAdmin):
    exclude = ()
    list_display = ('pk', 'image_thumbnail', 'title')
    readonly_fields = ('image_thumbnail',)

admin.site.register(Artwork, ArtworkForm)
admin.site.register(Artist)
admin.site.register(Crew)
admin.site.register(Artwork_Category)
admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(AlternativeImage)
admin.site.register(ArtistExpressionOfInterest, NewInfoForm)
admin.site.register(WallSpace, NewInfoForm)
admin.site.register(MuralCommission, NewInfoForm)
admin.site.register(Route, RouteForm)
admin.site.register(RoutePoint)
admin.site.register(Section)
admin.site.register(Logo, LogoForm)
# Register your models here.
