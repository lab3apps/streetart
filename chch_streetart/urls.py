"""chch_streetart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from streetart import views as streetart_views

urlpatterns = [
	url(r'^streetart/', include('streetart.urls')),
	url(r'^signup/$', streetart_views.signup, name='signup'),
	url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^settings/$', streetart_views.settings, name='settings'),
    url(r'^settings/password/$', streetart_views.password, name='password'),
    url(r'^', include('cms.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)