import decimal
import sys
import json
import datetime
import time
import urlparse
import urllib2
import requests
import flickrapi
import oauth2 as oauth
from math import ceil

import shapefile
import shapely
import numpy as np
from shapely.geometry import Polygon, Point as Point_S
from collections import Counter
from rtree import index

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from isprs import settings
from models import GPSData, FoursquareData, FSCircle, TwitterData, Lombardia



#Views to connect to APIs and create GPSData objects
def flickr(request, bbox='8.4931,44.9026,11.4316,46.6381', min_date=1451779200, max_date=1454198400):
    #FlickrAPI config connection
    flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET, format='json')
    #Handle redirect
    redirect(flickr.auth_via_url(perms='read'))
    response = flickr.photos.search(bbox=bbox, min_taken_date=min_date, max_taken_date=max_date, page=1)
    js = json.loads(response)
    count = 0
    #Iter over pages
    tot_pag=int(js['photos']['pages']+1)
    for p in range(1, tot_pag):
        #Request per page
        response = flickr.photos.search(bbox=bbox, min_taken_date=min_date, max_taken_date=max_date, page=p)
        js = json.loads(response)
        #Test if obj photos in response
        if js['photos'].get('photo'):
            for photo in js['photos']['photo']:
                geo = json.loads(flickr.photos.geo.getLocation(photo_id=photo['id']))
                info = json.loads(flickr.photos.getInfo(photo_id=photo['id']))
                taken = info['photo']['dates']['taken']
                posted = datetime.datetime.fromtimestamp(int(info['photo']['dates']['posted'])).strftime('%Y-%m-%d %H:%M:%S')
                #Create and save obj locall
                print photo['id']
                data = GPSData( latitude=float(geo['photo']['location']['latitude']), 
                                longitude=float(geo['photo']['location']['longitude']),
                                date_taken=taken,
                                date_posted=posted, user=info['photo']['owner']['username'],
                                local_id=photo['id'])
                data.save()

                #Count saved
                count += 1
        
    return HttpResponse('Finished! saved '+str(count))


def foursquare_circle(request):
    #Asks for areas of (14142*pi)^2 over the venues API of foursquare to cover fo the Lombardy region in Italy
    circles = FSCircle.objects.filter(radius=14142)
    for c in circles:
        url = 'https://api.foursquare.com/v2/venues/explore'
        url += '?client_id=%s&client_secret=%s&limit=50&intent=browse' % (settings.FOURSQUARE_CLIENT_ID, settings.FOURSQUARE_CLIENT_SECRET)
        url += '&v=20160101&m=foursquare'
        #Center and radius for each circle to cover the Lombardy region
        url += '&ll=%s,%s&radius=%s' % (c.latitude, c.longitude, c.radius)
        start = 0
        r = requests.get(url)
        if r.status_code == 200:

            js = json.loads(r.content)
            top = int(ceil(js['response']['totalResults']/50))

            for item in js['response']['groups'][0]['items']:
                venue = item['venue']
                if (venue['hereNow']['count'] > 0):
                    
                    fs_data = FoursquareData(   checkin_count=venue['stats']['checkinsCount'], here_now=venue['hereNow']['count'],
                                                postal_code=venue['location'].get('postalCode', None), category=venue['categories'][0]['name'], 
                                                venue=venue['name'], radius=c.radius)

                    fs_data.save()
                    data = GPSData( latitude=venue['location']['lat'], longitude=venue['location']['lng'], date_taken=datetime.datetime.now(), 
                                    platform=GPSData.FOURSQUARE, fs_data=fs_data)
                    data.save()
            #Iter pages
            for i in range(top-1):
                start += 50
                url += '&offset='+str(start)
                r = requests.get(url)
                if r is not None:
                    js = json.loads(r.content)
                    #Iter results
                    for item in js['response']['groups'][0]['items']:
                        venue = item['venue']
                        if (venue['hereNow']['count'] > 0):
                            
                            #Create local object with the json fields
                            fs_data = FoursquareData(   checkin_count=venue['stats']['checkinsCount'], here_now=venue['hereNow']['count'],
                                                        postal_code=venue['location'].get('postalCode', None), category=venue['categories'][0]['name'],
                                                        venue=venue['name'])
                            fs_data.save()
                            data = GPSData( latitude=venue['location']['lat'], longitude=venue['location']['lng'], date_taken=datetime.datetime.now(), 
                                            platform=GPSData.FOURSQUARE, fs_data=fs_data)
                            data.save()
        GPSData.del_dups()
        GPSData.gen_fs_dups()


    return HttpResponse('Finished!\nlast response: </br>'+r.content)

def twitter(request, bbox='6.63,36.46,18.78,47.09'):
    #url for streaming API limited to the bounding box for Italy/bbox can also be a URL param
    country = "ITA"
    url = "https://stream.twitter.com/1.1/statuses/filter.json?locations=%s" % (bbox)
    if bbox.split(',')[0] == '38.941': #if bbox is tanzania add also flood words in swahili
        "&track=%s" % 'mafuriko,gharika'
        country = "TZN"

    print url
    
    #Reads the twitter live response

    backoff_network_error = 0.25
    backoff_http_error = 5
    backoff_rate_limit = 60
    while True:
        try:
            stream = oauth_req(url)
            for line in stream:
                handle_tweets(line, country) #Saves tweet
        except:
            # Network error, use linear back off up to 16 seconds
            #print 'Network error: %s' % stream or "no stream!"
            print 'Waiting %s seconds before trying again' % backoff_network_error
            time.sleep(backoff_network_error)
            backoff_network_error = min(backoff_network_error + 1, 16)
            continue
        # HTTP Error
        sc = stream.getcode()
        if sc == 420:
            # Rate limit, use exponential back off starting with 1 minute and double each attempt
            print 'Rate limit, waiting %s seconds' % backoff_rate_limit
            time.sleep(backoff_rate_limit)
            backoff_rate_limit *= 2
        else:
            # HTTP error, use exponential back off up to 320 seconds
            print 'HTTP error %s, %s' % (sc, stream.getcode())
            print 'Waiting %s seconds' % backoff_http_error
            time.sleep(backoff_http_error)
            backoff_http_error = min(backoff_http_error * 2, 320)

        

        
    return HttpResponse('Finished!\nlast response: </br>'+"<a href='"+str(stream)+"' >"+str(stream)+"</a>")

def handle_tweets(line, country):
    if line.endswith('\r\n'):
            try:
                 tweet = json.loads(line)
                 #Only saves the gereferenced tweets
                 if tweet.get('coordinates'):
                    tweet_db = TwitterData( latitude=tweet['coordinates']['coordinates'][1], longitude=tweet['coordinates']['coordinates'][0],
                                            user=tweet['user']['screen_name'], date=datetime.datetime.strptime(str(tweet['created_at']), "%a %b %d %H:%M:%S +%f %Y"),
                                            text=tweet['text'], country=country)
                    if tweet.get('source'):
                        tweet_db.source = tweet['source']
                    if tweet['user'].get('location'):
                        tweet_db.user_location = tweet['user']['location']
                    if tweet.get('entities'):
                        hashtags = ''
                        for ht in tweet['entities']['hashtags']:
                            hashtags += ht['text'] + ","
                        tweet_db.hashtags = hashtags
                    tweet_db.save()
                    print 'Coordinates! ' + str(tweet['coordinates']['coordinates'])
                 #else:
                  #  print tweet
            except:
                print "::Not saved!: %s" % line


#Handles twitter oauth and send requests
def oauth_req(url, http_method="GET", post_body="", http_headers=None):
    consumer = oauth.Consumer(key=settings.TWITTER_API_KEY, secret=settings.TWITTER_CONSUMER_SECRET)
    token = oauth.Token(key=settings.TWITTER_TOKEN_KEY, secret=settings.TWITTER_TOKEN_SECRET)
    client = oauth.Client(consumer, token)
    params = {
    'oauth_version': "1.0",
    'oauth_nonce': oauth.generate_nonce(),
    'oauth_timestamp': str(int(time.time())),
    }
    params['oauth_token'] = token.key
    params['oauth_consumer_key'] = consumer.key
    req = oauth.Request(method=http_method, url=url, parameters=params)
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    #signes request
    req.sign_request(signature_method, consumer, token)
    #sends request
    rs = urllib2.urlopen(req.to_url())
    return rs
 
  
def json_OL_heatmap(request, days=2, platform='FSQ', date_start=None, date_end=None, keyword=''):
    """Feeds an OpenLayers client to display data as heatmap"""
    #Load the shapefile of polygons and convert it to shapely polygon objects
    polygons_sf = shapefile.Reader("static/shapefile/griglia_0_02.shp")
    #polygons_sf = shapefile.Reader("shapefile/test.shp")
    polygon_shapes = polygons_sf.shapes()
    polygon_points = [q.points for q in polygon_shapes ]
    polygons = [Polygon(q) for q in polygon_points]

    idx = index.Index()
    count = -1
    for q in polygon_shapes:
        count +=1
        idx.insert(count, q.bbox)

    #Create a list of cell ID 
    poly_index = [i for i in range(len(polygons))]

    # Compute the coordinates of the grid centres and put them into lat/lon lists
    lat_centres = list()
    lon_centres = list()
    polygon_points_np = np.array(polygon_points)

    for i in range(max(polygon_points_np.shape)):  
        x_min = polygon_points_np[i][0][0];
        x_max = polygon_points_np[i][1][0];
        y_min = polygon_points_np[i][2][1];
        y_max = polygon_points_np[i][1][1];
        x_cent= (x_max-x_min)/2 + x_min;
        y_cent= (y_max-y_min)/2 + y_min;
        lon_centres.append(x_cent)
        lat_centres.append(y_cent)

    if date_start is None and date_end is None:
        #Get the points HERE!!!
        #print cache.get(platform)
        if cache.get(platform) is not None:
            print "using cache!", platform
            data = cache.get(platform)
        else:
            print "setting cache", platform
            if platform == 'TWT':
                data = TwitterData.objects.filter(date__range=(datetime.date.today()-datetime.timedelta(days=days), datetime.date.today()))
                if keyword != None:
                    data = data.filter(text__contains=keyword)
            else:
                data = GPSData.objects.filter(platform=platform, date_taken__range=(datetime.date.today()-datetime.timedelta(days=days), datetime.date.today()))
            cache.set(platform, data, 172800)
    else:
        date_start = date_start+"_00:00:00"
        date_end = date_end+"_00:00:00"
        if cache.get(platform+str(date_start)+"_"+str(date_end)) is not None and keyword is None:
            data = cache.get(platform+str(date_start)+"_"+str(date_end))
        else:
            if platform == 'TWT':
                data = TwitterData.objects.filter(date__range=(datetime.datetime.strptime(date_start, '%d-%m-%Y_%H:%M:%S'), datetime.datetime.strptime(date_end, '%d-%m-%Y_%H:%M:%S')))
                if keyword is not None:
                    data = data.filter(text__contains=keyword)
            else:
                data = GPSData.objects.filter(platform=platform, date_taken__range=(datetime.datetime.strptime(date_start, '%d-%m-%Y_%H:%M:%S'), datetime.datetime.strptime(date_end, '%d-%m-%Y_%H:%M:%S')))
                if platform == 'FSQ' and keyword is not None:
                    data = data.filter(fs_data__category = keyword)
            if keyword is None:
                cache.set(platform+str(date_start)+"_"+str(date_end), data, 172800)
    
    point_coords = [[obj.longitude, obj.latitude] for obj in data]
    points = [Point_S(q) for q in point_coords]

    #Assign one or more matching polygons to each point
    matches = []
    for i in range(len(points)): #Iterate through each point
        temp = None
        #Iterate only through the bounding boxes which contain the point
        for j in idx.intersection( point_coords[i]):
            #Verify that point is within the polygon itself not just the bounding box
            if points[i].within(polygons[j]):
                #print "Match found! ",j
                temp=j
                break
        matches.append(temp) #Either the first match found, or None for no matches

    #Create a dictionary containing the counts of points in the cells
    count = dict(Counter(matches))

    #Create a list of the counts to be associated to any cell ID
    d = list()
    for i in range(len(poly_index)):
        if poly_index[i] in count:
           d.append(count[i])
        else:
           d.append(0)
 
    #Write the JS variable to feed the Heatmap
    jfile = dict()
    jfile['max'] = max(d)
    ps = list()
    for i in range(len(poly_index)):
        if d[i] != 0:
            ps.append({'lat': lat_centres[i], 'lng': lon_centres[i], 'count': d[i]})
    jfile['data'] = ps

    return JsonResponse(jfile)

def heatmap(request):
    return render(request, 'index.html')