import chch_streetart.wsgi
from streetart.models import Artwork, Artist, Artwork_Category, Crew, Status
import json
from django.core.files import File  # you need this somewhere
import urllib
import csv

artists = {}
artworks = {}
artwork_categories = {}
crews = {}
statuses = {}
routes = {}

def newArtwork(artistData,routeData,title,imageURL,photo_credit,city,locationLon,locationLat,
	link,crew,category,status,decommission_date,commission_date,description):

	artwork = Artwork()

	for artist in getArtists(artistData):
		artwork.artists.add(artist)
	artwork.status = getStatus(status)
	artwork.crew = getCrew(crew)
	artwork.category = getCategory(category)
	addRoutes(routeData)

	artwork.title = title
	artwork.commission_date = commission_date
	artwork.decommission_date = decommission_date
	artwork.description = description
	# Need to figure a way to pull the image from the url and to then put it into the database.
	result = urllib.urlretrieve(imageURL)
	artwork.image.save(
    	os.path.basename(imageURL),
    	File(open(result[0]))
    )
	artwork.photo_credit = photo_credit
	artwork.location.longitude = locationLon
	artwork.location.latitude = locationLat
	artwork.city = city
	artwork.link = link
	artwork.save()

def getStatus(status):
	if status in statuses:
		return statuses[status]
	else:
		_status = Status()
		_status.name = status
		_status.save()
		statuses[status] = _status
		return _status
		
def getCrew(crew):
	if crew in crews:
		return crews[crew]
	else:
		_crew = Crew()
		_crew.name = crew
		_crew.save()
		crews[crew] = _crew
		return _crew

def getCategory(category):
	if category in artwork_categories:
		return artwork_categories[category]
	else:
		artwork_category = Artwork_Category()
		artwork_category.name = category
		artwork_category.save()
		artwork_categories[category] = artwork_category
		return artwork_category

def addRoutes(routeData):

	return None

def getArtists(artistData):
	names = artistData['name'].split(',')
	artists_ = []
	for name in names:
		name = name.strip(' ')
		if name in artists:
			artists_.append(artists[name])
		else:
			if len(names) > 1:
				website = None
				facebook = None
				insta = None
				twitter = None
				otherlinks = None
			else:
				artist_from = artistData['from']
				website = artistData['website']
				facebook = artistData['facebook']
				insta = artistData['insta']
				twitter = None
				otherlinks = artistData['otherlinks']
			artist_ = newArtist(name,website,facebook,insta,twitter,artist_from,otherlinks)
			artists_.append(artist_)
	return artists_

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
	artists['name'] = artist
	return artist


# title,imageURL,photo_credit,city,locationLon,locationLat,
# 	link=None,artists=None,crew=None,
# 	category=None,status=None,decommission_date=None,commission_date=None,description=None

def csvimport():
	with open('streetart_database_for_new_website.csv', 'r') as f:
		reader = csv.reader(f)
		data = list(reader)
	headerdata = data[0]
	for row in data[1:-1]:
		#'FID', 'artwork_name', 'artist_name', 'crew',
		#'Artist_from', 'WTS_status', 'status', 'Category', 'Commissioned_by', 
		#'Commission_date', 'Decommission_date', 'Recommended_route', 
		#'Order_in_route', 'descriptio', 'Website', 'Instagram', 'Facebook', 
		#'pic_url', 'Photo_credit', 'GlobalID', 'CreationDa', 'Creator', 'EditDate', 'Editor', 'LinksUnk', 'x', 'y', 'City'
		print(row)
		artistData = {
					'name':row[headerdata.index('artist_name')],
					'from':row[headerdata.index('Artist_from')],
					'website':row[headerdata.index('Website')],
					'insta':row[headerdata.index('Instagram')],
					'facebook':row[headerdata.index('Facebook')],
					'otherlinks':row[headerdata.index('LinksUnk')]
					}
		title = row[headerdata.index('artwork_name')]
		imageURL = row[headerdata.index('pic_url')]
		photo_credit = row[headerdata.index('Photo_credit')]
		city = row[headerdata.index('City')]
		locationLon = row[headerdata.index('x')]
		locationLat = row[headerdata.index('y')]
		link = None
		crew = row[headerdata.index('crew')]
		category = row[headerdata.index('Category')]
		status = row[headerdata.index('status')]
		decommission_date = row[headerdata.index('Decommission_date')]
		commission_date = row[headerdata.index('Commission_date')]
		description = row[headerdata.index('descriptio')]
		routeData = {'route':row[headerdata.index('Recommended_route')], 'position':row[headerdata.index('Order_in_route')]}
		newArtwork()

def jsonimport():
	with open('lab3_json_2017-08-16.geojson') as f:
		data = json.load(f)

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


csvimport()