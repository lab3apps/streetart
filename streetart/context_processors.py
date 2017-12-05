from django.conf import settings

def global_settings(request):
    return {
        'google_api_key': settings.GOOGLE_MAPS_API_KEY,
        'city': settings.CITY,
        'SOCIAL_AUTH_FACEBOOK_KEY': settings.SOCIAL_AUTH_FACEBOOK_KEY
    }