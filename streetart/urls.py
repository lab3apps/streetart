from django.conf.urls import url, include

from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ArtworkCreateView, ArtistCreateView

app_name = 'streetart'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^artwork/new/$', views.add_new, name='new_artwork'),
	url(r'^muralcommision/new/$', views.add_new, name='new_muralcommission'),
	url(r'^wallspace/new/$', views.add_new, name='new_wallspace'),
	url(r'^artistexpressionofinterest/new/$', views.add_new, name='new_artistexpressionofinterest'),
	url(r'^getdata/([0-9]+)/$', views.closest_artwork, name='closest_artwork'),
	url(r'^imageselected/([0-9]+)/$', views.image_selected, name='image_selected'),
    url(r'^artworks/$', ArtworkCreateView.as_view(), name='create_artwork'),
    url(r'^artists/$', ArtistCreateView.as_view(), name='create_artist'),
    url(r'^like/$', views.like, name='like'),
]

urlpatterns = format_suffix_patterns(urlpatterns)