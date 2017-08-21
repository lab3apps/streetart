from django.conf.urls import url, include

from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView

app_name = 'streetart'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^artwork/new/$', views.new_artwork, name='new_artwork'),
	url(r'^getdata/([0-9]+)/$', views.closest_artwork, name='closest_artwork')
    url(r'^artworks/$', CreateView.as_view(), name='create'),
]

urlpatterns = format_suffix_patterns(urlpatterns)