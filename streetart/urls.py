from django.conf.urls import url, include

from . import views

app_name = 'streetart'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^artwork/new/$', views.new_artwork, name='new_artwork'),
	url(r'^getdata/([0-9]+)/$', views.closest_artwork, name='closest_artwork')
]