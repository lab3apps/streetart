from django.contrib import admin
from .models import Question
from .models import Choice
from .models import Artwork
from .models import Artist
from .models import Crew
from .models import Artwork_Category

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Artwork)
admin.site.register(Artist)
admin.site.register(Crew)
admin.site.register(Artwork_Category)
# Register your models here.
