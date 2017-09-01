import chch_streetart.wsgi
from streetart.models import Artwork, Artist, Artwork_Category, Crew, Status
import json
from django.core.files import File  # you need this somewhere
import urllib.request
import csv
import os
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point

artists = {}
artworks = {}
artwork_categories = {}
crews = {}
statuses = {}
routes = {}

def newArtwork(artistData,routeData,title,imageURL,photo_credit,city,locationLon,locationLat,
	link,crew,category,status,decommission_date,commission_date,description):
	if imageURL.strip() == '':
		return

	artwork = Artwork()

	artwork.title = title
	artwork.commission_date = commission_date
	print(artwork.title)
	print(title)
	print(artwork.commission_date)
	artwork.decommission_date = decommission_date
	artwork.description = description[:49]
	# Need to figure a way to pull the image from the url and to then put it into the database.
	result = urllib.request.urlretrieve(imageURL)
	artwork.photo_credit = photo_credit
	print(locationLon, locationLat)
	artwork.location = Point(float(locationLon), float(locationLat))
	# y = locationLat
	# artwork.location.x = locationLon
	
	artwork.city = city
	artwork.link = link
	artwork.category = getCategory(category)
	addRoutes(routeData)
	artwork.status = getStatus(status)
	artwork.image.save(
    	os.path.basename(imageURL),
    	File(open(result[0], 'rb'))
    )
	for artist in getArtists(artistData):
		artwork.artists.add(artist)
	for crew in getCrew(crew):
		artwork.crews.add(crew)
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
		
def getCrew(crewdata):
	_crews = crewdata.split(',')
	crews_ = []
	for crew in _crews:
		crew = crew.strip(' ')
		if crew in crews:
			crews_.append(crews[crew])
		else:
			_crew = Crew()
			_crew.name = crew
			_crew.city = ''
			_crew.is_disbanded = False
			_crew.formed_date = '2017-01-01'
			_crew.save()
			crews[crew] = _crew
	return crews_

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
				website = artistData['website']
				facebook = artistData['facebook']
				insta = artistData['insta']
				twitter = None
				otherlinks = artistData['otherlinks']
			artist_from = artistData['from']
			if artist_from.strip() == '':
				artist_from = 'Unknown'
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
	print(headerdata)
	for row in data[1:-1]:
		#'FID', 'artwork_name', 'artist_name', 'crew',
		#'Artist_from', 'WTS_status', 'status', 'Category', 'Commissioned_by', 
		#'Commission_date', 'Decommission_date', 'Recommended_route', 
		#'Order_in_route', 'descriptio', 'Website', 'Instagram', 'Facebook', 
		#'pic_url', 'Photo_credit', 'GlobalID', 'CreationDa', 'Creator', 'EditDate', 'Editor', 'LinksUnk', 'x', 'y', 'City'
		print(row)
		artistData = {
					'name':row[headerdata.index('artist_name')],
					'from':row[headerdata.index('artist_from')],
					'website':row[headerdata.index('website')],
					'insta':row[headerdata.index('instagram')],
					'facebook':row[headerdata.index('facebook')],
					'otherlinks':row[headerdata.index('links')]
					}
		title = row[headerdata.index('artwork_name')]
		imageURL = row[headerdata.index('pic_url')]
		photo_credit = row[headerdata.index('photo_credit')]
		city = row[headerdata.index('city')]
		locationLon = row[headerdata.index('x')]
		locationLat = row[headerdata.index('y')]
		link = None
		crew = row[headerdata.index('crew')]
		category = row[headerdata.index('category')]
		status = row[headerdata.index('status')]
		decommission_date = row[headerdata.index('decommission_date')]
		commission_date = row[headerdata.index('commission_date')]
		#if decommission_date.strip(' ') == '':
		decommission_date = None
		#if commission_date.strip(' ') == '':
		commission_date = None
		description = row[headerdata.index('description')]
		routeData = {'route':row[headerdata.index('recommended_route')], 'position':row[headerdata.index('Order_in_route')]}
		try:
			newArtwork(artistData,routeData,title,imageURL,photo_credit,city,locationLon,locationLat,
				link,crew,category,status,decommission_date,commission_date,description)
		except:
			print(row)


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