from django.contrib import admin
from .models import Artwork, Artist, Crew, Artwork_Category, Profile, Status, AlternativeImage, ArtistExpressionOfInterest, Feedback, WallSpace, MuralCommission, Route, RoutePoint, GetInvolved, WhatsNew, Logo, Page, Media, FeaturedVideo
from mapwidgets.widgets import GooglePointFieldWidget
from django import forms
from django.contrib.gis.db import models
from adminsortable2.admin import SortableInlineAdminMixin
from image_cropping import ImageCroppingMixin
from django_summernote.widgets import SummernoteWidget   


class ImageAdmin(admin.TabularInline):
    model = AlternativeImage
    readonly_fields = ('image_thumbnail',)

class ArtworkForm(ImageCroppingMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    fields = ('title', 'validated', 'map_enabled', 'smart_cities', 'status', 'artists', 'crews', 'category', 'description', 'commission_date', 'decommission_date', 'image', 'photo_credit', 'cropping', 'image_thumbnail', 'city', 'link', 'video_url', 'location', 'street', 'admin_notes', 'submitter_description', 'submitter_name', 'submitter_email')
    exclude = ('likes', 'checkins', 'cropped_image', 'watermarked_image')
    filter_horizontal = ('artists', 'crews')
    list_display = ('pk', 'image_thumbnail', 'title', 'get_artists', 'validated', 'status')
    inlines = [ ImageAdmin ]
    readonly_fields = ('image_thumbnail',)
    search_fields = ['title', 'artists__name', 'description']

class NewInfoForm(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    readonly_fields = ('created',)

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

class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        widgets = {
            'page_content': SummernoteWidget(),
        }
        exclude = ('slug',) 

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm

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
admin.site.register(Feedback, NewInfoForm)
admin.site.register(Route, RouteForm)
admin.site.register(RoutePoint)
admin.site.register(GetInvolved)
admin.site.register(WhatsNew)
admin.site.register(Media)
admin.site.register(Logo, LogoForm)
admin.site.register(Page, PageAdmin)
admin.site.register(FeaturedVideo)
# Register your models here.
