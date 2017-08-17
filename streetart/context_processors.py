from django.conf import settings

def global_settings(request):
    return {
        'google_api_key': settings.GEOPOSITION_GOOGLE_MAPS_API_KEY,
    }