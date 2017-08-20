from django.contrib import admin
from .models import Artwork
from .models import Artist
from .models import Crew
from .models import Artwork_Category
from .models import Profile

admin.site.register(Artwork)
admin.site.register(Artist)
admin.site.register(Crew)
admin.site.register(Artwork_Category)
admin.site.register(Profile)
# Register your models here.
