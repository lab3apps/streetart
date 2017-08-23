import chch_streetart.wsgi
from streetart.models import Artwork, Artist
import json
from django.core.files import File  # you need this somewhere
import urllib

with open('lab3_json_2017-08-16.geojson') as f:
    data = json.load(f)

artists = {}
artworks = {}

def newArtwork(title,imageURL,photo_credit,city,locationLon,locationLat,
	link=None,artists=None,crew=None,thumbnailURL=None,
	category=None,status=None,decommission_date=None,commission_date=None,description=None):

	artwork = Artwork()

	artwork.artists = getArtists(artists)
	artwork.crew = crew
	artwork.category = category
	artwork.title = title
	artwork.commission_date = commission_date
	artwork.status = status
	artwork.decommission_date = decommission_date
	artwork.description = description
	# Need to figure a way to pull the image from the url and to then put it into the database.
	result = urllib.urlretrieve(imageURL)
	artwork.image.save(
    	os.path.basename(imageURL),
    	File(open(result[0]))
    )
	artwork.photo_credit = photo_credit
	# same as image.
	#artwork.thumbnail = 
	artwork.location.longitude = locationLon
	artwork.location.latitude = locationLat
	artwork.city = city
	artwork.link = link
	artwork.save()

def getArtists(artists):
	for x in artists:
		newArtist(x)

def newArtist(name, website, facebook, insta, twitter, artist_from, otherlinks):
	artist = Artist()
	artist.name = name
	artist.website = website
	artist.facebook = facebook
	artist.instagram = insta
	artist.twitter = twitter
	artist.artist_from = artist_from
	artist.other_links = otherlinks
	artist.save()

for feature in data['features']:
	for key, value in feature.items():
		if key == 'geometry':
			geometry = value['coordinates']
			print(geometry)
	for key2, value2 in feature['properties'].items():
		if value2 == None:
			continue
		if key2 == 'Commission_Date':
			commission_date = value2
			continue
		elif key2 == 'Decommission_Date':
			decommission_date = value2
		elif key2 == 'pic_url':
			imageURL = value2
			print(imageURL)
		elif key2 == 'name':
			name = value2.split('<')[0]
			print(name)
		elif key2 == 'thumb_url':
			thumbnailURL = value2
		elif key2 == 'description':
			description = ''
			i = True
			for char in value2:
				if char == '<':
					i = False
				if i:
					description += char
				if char == '>':
					i = True
			if 'More about the artist...' in description:
				description = description.split('More about the artist...')[0]
			print(description)

		#print(key2, ':', value2)
	#break
	# if 'description' in feature:
	# 	print(feature['description'])

