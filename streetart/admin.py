import textwrap

from django.contrib import admin
from .models import Artwork, Artist, Crew, Artwork_Category, Profile, Status, AlternativeImage, ArtistExpressionOfInterest, WallSpace, MuralCommission, Route, RoutePoint, GetInvolved, WhatsNew, Logo, Page, Media, Feedback
from mapwidgets.widgets import GooglePointFieldWidget
from django import forms
from django.contrib.gis.db import models
from adminsortable2.admin import SortableInlineAdminMixin
from image_cropping import ImageCroppingMixin
from django_summernote.widgets import SummernoteWidget   
from import_export.admin import ImportExportModelAdmin

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

class ArtworkForm(ImageCroppingMixin,ImportExportModelAdmin):
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

class ArtistForm(ImportExportModelAdmin):
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

class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        widgets = {
            'page_content': SummernoteWidget(),
        }
        exclude = ('slug',) 

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm


class CrewForm(ImportExportModelAdmin):
    class Meta:
        model = Crew


class ArtworkCategoryForm(ImportExportModelAdmin):
    class Meta:
        model = Artwork_Category

class AlternativeImagesForm(ImportExportModelAdmin):
    list_display = ('pk','artwork', 'image_thumbnail')

    class Meta:
        model = AlternativeImage

class FeedbackForm(ImportExportModelAdmin):
    list_display = ('pk', 'email', 'category', 'subject', 'message')

    class Meta:
        model = Feedback

## Export Module

admin.site.register(Artwork, ArtworkForm)
admin.site.register(Artist, ArtistForm)
admin.site.register(Crew, CrewForm)
admin.site.register(Artwork_Category, ArtworkCategoryForm)
admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(AlternativeImage, AlternativeImagesForm)
admin.site.register(ArtistExpressionOfInterest, NewInfoForm)
admin.site.register(WallSpace, NewInfoForm)
admin.site.register(MuralCommission, NewInfoForm)
admin.site.register(Route, RouteForm)
admin.site.register(RoutePoint, RoutePointForm)
admin.site.register(GetInvolved)
admin.site.register(WhatsNew)
admin.site.register(Media)
admin.site.register(Feedback, FeedbackForm)
admin.site.register(Logo, LogoForm)
admin.site.register(Page, PageAdmin)
# Register your models here.
