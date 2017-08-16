import chch_streetart.wsgi
from streetart.models import Artwork
import json


with open('lab3_json_2017-08-16.geojson') as f:
    data = json.load(f)

for feature in data['features']:
	for key, value in feature.items():
		print(key, value)
	for key2, value2 in feature['properties'].items():
		print(key2, value2)
	break
	if 'description' in feature:
		print(feature['description'])
	# artwork = Artwork()
	# artwork.artist = 
	# artwork.crew = 
	# artwork.category = 
	# artwork.name = 
	# artwork.commission_date =
	# artwork.status = 
	# artwork.decommission_date = 
	# artwork.description = 
	# artwork.image = 
	# artwork.photo_credit = 
	# artwork.thumbnail = 
	# artwork.longitude = 
	# artwork.latitude = 
	# artwork.city = 
	# artwork.link = 
	# artwork.save()

