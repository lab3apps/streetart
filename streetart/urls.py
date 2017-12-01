from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

app_name = 'streetart'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^about/$', RedirectView.as_view(url='/blog/about', permanent=True), name='about'),
	url(r'^artwork/(?P<pk>[0-9]+)$', views.home, name='image_selected'),
	url(r'^artwork/new/$', views.add_new, name='new_artwork'),
	url(r'^muralcommision/new/$', views.add_new, name='new_muralcommission'),
	url(r'^wallspace/new/$', views.add_new, name='new_wallspace'),
	url(r'^artistexpressionofinterest/new/$', views.add_new, name='new_artistexpressionofinterest'),
	url(r'^nearby/([0-9]+)/$', views.closest_artwork, name='closest_artwork'),
	url(r'^nearby/(?P<lat>-?\d+.?\d+)/(?P<lng>-?\d+.?\d+)$', views.closest_artworks_from_user, name='closest_artwork from User'),
	url(r'^imageselected/([0-9]+)/$', views.image_selected, name='image_selected'),
    url(r'^artworks/$', views.artwork_list, name='artwork_list'),
	url(r'^allartworks/$', views.get_artworks_as_json, name='allartwork_list'),
    url(r'^artworks/(?P<pk>[0-9]+)$', views.artwork_detail, name='artwork_detail'),
    url(r'^artists/$', views.artist_list, name='artist_list'),
    url(r'^artists/(?P<pk>[0-9]+)$', views.artist_detail, name='artist_detail'),
	url(r'^page/(?P<slug>[\w-]+)/$', views.page, name='page'),
    url(r'^routes/$', views.route_list, name='route_list'),
    url(r'^routes/(?P<pk>[0-9]+)$', views.route_detail, name='route_detail'),
    url(r'^like/([0-9]+)/$', views.like, name='like'),
	url(r'^checkin/([0-9]+)/$', views.checkIn, name='checkIn'),
	url(r'^thanks/$', views.thanks, name='thanks'),
	url(r'^logos/$', views.logos, name='thanks'),
	url(r'^donate/$', RedirectView.as_view(url='/page/donate', permanent=True), name='donate'),
	url(r'^get-involved/$', views.home, name='getinvolved'),
	url(r'^post-comment/$', views.post_comment, name='post_comment'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
