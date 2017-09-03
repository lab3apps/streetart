import chch_streetart.wsgi
from streetart.models import Artwork, Artist, Artwork_Category, Crew, Status, Route
from django.template.defaultfilters import slugify


def change_artwork_slug():
	all_artworks = Artwork.objects.all()
	for artwork in all_artworks:
		if artwork.slug == '' or artwork.slug == None:
			slug_ = slugify(artwork.pk)
			print(slug_)
			artwork.slug = slug_
			artwork.save()

change_artwork_slug()