import chch_streetart.wsgi
from streetart.models import Artwork
import json


with open('lab3_json_2017-08-16.geojson') as f:
    data = json.load(f)

artists = {}
artworks = {}

def newArtwork(artist=None,crew=None,category,name,
	commission_date,status,decommission_date,description,
	imageURL,photo_credit,thumbnailURL=None,city,
	link,locationLon,locationLat):
	artwork = Artwork()
	artwork.artist = artist
	artwork.crew = crew
	artwork.category = category
	artwork.name = name
	artwork.commission_date = commission_date
	artwork.status = status
	artwork.decommission_date = decommission_date
	artwork.description = description
	# Need to figure a way to pull the image from the url and to then put it into the database.
	#artwork.image = 
	artwork.photo_credit = photo_credit
	# same as image.
	#artwork.thumbnail = 
	artwork.location.longitude = locationLon
	artwork.location.latitude = locationLat
	artwork.city = city
	artwork.link = link
	artwork.save()

for feature in data['features']:
	for key, value in feature.items():
		print(key, value)
	for key2, value2 in feature['properties'].items():
		print(key2, value2)
	break
	if 'description' in feature:
		print(feature['description'])

