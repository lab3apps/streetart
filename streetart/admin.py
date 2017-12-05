import textwrap

from django.contrib import admin
from .models import Artwork, Artist, Crew, Artwork_Category, Profile, Status, AlternativeImage, ArtistExpressionOfInterest, WallSpace, MuralCommission, Route, RoutePoint, GetInvolved, WhatsNew, Logo
from mapwidgets.widgets import GooglePointFieldWidget
from django import forms
from django.contrib.gis.db import models
from adminsortable2.admin import SortableInlineAdminMixin
from image_cropping import ImageCroppingMixin


class ImageAdmin(admin.TabularInline):
    model = AlternativeImage
    readonly_fields = ('image_thumbnail',)

def enable_on_map(modeladmin, request , queryset):
    queryset.update(map_enabled=True)

def disable_on_map(modeladmin, request , queryset):
    queryset.update(map_enabled=False)

def show_for_smart_cities(modeladmin, request , queryset):
    queryset.update(smart_cities=True)

def hide_for_smart_cities(modeladmin, request, queryset):
    queryset.update(smart_cities=False)

class ArtworkForm(ImageCroppingMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    def shortTitle(self,obj):
        if obj.title is None:
            return " - - NO Data - - "
        else:
            striped = obj.title.strip()
            length = len(striped)
            if 1 < length < 27:
                return striped
            elif length <= 0:
                return " - - Empty - - "
            else:
                return textwrap.shorten(obj.title, 27, placeholder="...")
    shortTitle.short_description = "Title"

    def map(self,obj):
        if obj.map_enabled:
            return "Yes"
        else:
            return  "No"

    def smartcity(self, obj):
        if obj.smart_cities:
            return "Yes"
        else:
            return "No"

    smartcity.short_description="S.City"
    exclude = ('likes', 'checkins', 'cropped_image', 'watermarked_image')
    filter_horizontal = ('artists', 'crews')
    list_display = ('pk', 'image_thumbnail', 'shortTitle', 'get_artists', 'map', 'smartcity', 'validated', 'status')
    list_editable = ('validated', 'status',)
    inlines = [ImageAdmin]
    readonly_fields = ('image_thumbnail',)
    search_fields = ['title', 'artists__name', 'description']
    actions = [show_for_smart_cities, hide_for_smart_cities, enable_on_map, disable_on_map]
    class Meta:
        model = Artwork

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

class RoutePointForm(admin.ModelAdmin):

    list_display = ('route', 'artwork', 'route_order', 'imagetag')

    class Meta:
        model = RoutePoint

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
admin.site.register(RoutePoint, RoutePointForm)
admin.site.register(GetInvolved)
admin.site.register(WhatsNew)
admin.site.register(Logo, LogoForm)
# Register your models here.
