import chch_streetart.wsgi
from streetart.models import Artwork, Artist, Artwork_Category, Crew, Status, Route
from django.template.defaultfilters import slugify


def change_artwork_slug:
	all_artworks = Artwork.objects.all()
	for artwork in all_artworks:
		if artwork.slug == '' or artwork.slug == None:
			artwork.slug = slugify(artwork.pk)
			artwork.save()

change_artwork_slug()