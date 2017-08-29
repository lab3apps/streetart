from django.conf.urls import url, include

from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ArtworkCreateView, ArtistCreateView

app_name = 'streetart'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^artwork/new/$', views.new_artwork, name='new_artwork'),
	url(r'^getdata/([0-9]+)/$', views.closest_artwork, name='closest_artwork'),
	url(r'^imageselected/([0-9]+)/$', views.image_selected, name='image_selected'),
    url(r'^artworks/$', ArtworkCreateView.as_view(), name='create_artwork'),
    url(r'^artists/$', ArtistCreateView.as_view(), name='create_artist'),
    url(r'^like/$', views.like, name='like'),
	url(r'^checkin/$', views.checkIn, name='checkIn'),
]

urlpatterns = format_suffix_patterns(urlpatterns)