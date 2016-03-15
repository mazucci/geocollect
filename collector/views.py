import decimal
import json
import datetime
import urlparse
import urllib2
import requests
import flickrapi
import oauth2 as oauth
from math import ceil

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from isprs import settings
from models import *



#Views to connect to APIs and create GPSData objects
def flickr(request, bbox='8.4931,44.9026,11.4316,46.6381', min_date=1439596800, max_date=1441065599):
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
                #Create and save obj locally
                data = GPSData( latitude=float(geo['photo']['location']['latitude']), 
                                longitude=float(geo['photo']['location']['longitude']),
                                date_taken=taken,
                                date_posted=posted, user=info['photo']['owner']['username'] )
                data.save()

                #Count saved
                count += 1
        
    return HttpResponse('Finished! saved '+str(count))


def panoramio(request):
    start = 0
    phcount = start
    url = "http://www.panoramio.com/map/get_panoramas.php?set=full&from=%s&to=%s" % (start, start+100)
    url += "&minx=%s&miny=%s&maxx=%s&maxy=%s&size=medium&mapfilter=no" % (8.4931,44.9026,11.4316,46.6381) #bounding box
    r = requests.get(url)
    #Response ok?
    if r.status_code == 200:

        js = json.loads(r.content)
        for photo in js['photos']:
            data = GPSData( latitude=round(photo['latitude'],6), longitude=round(photo['longitude'],6), 
                            date_posted=datetime.datetime.strptime(photo['upload_date'], "%d %B %Y"),
                            platform=GPSData.PANORAMIO,
                            user=photo['owner_name'])
            data.save()
            phcount+=1
        #Iter over pages
        while js['has_more'] is True:
            #Last photo index saved + 1
            start = phcount + 1
            #ask for 100 photos more
            url = "http://www.panoramio.com/map/get_panoramas.php?set=full&from=%s&to=%s" % (start, start+100)
            url += "&minx=%s&miny=%s&maxx=%s&maxy=%s&size=medium&mapfilter=no" % (6.8640, 44.0994, 12.6807, 46.1532)
            r = requests.get(url)
            
            if r is not None:
                js = json.loads(r.content)
                for photo in js['photos']:
                    data = GPSData( latitude=round(photo['latitude'],6), longitude=round(photo['longitude'],6), 
                                    date_posted=datetime.datetime.strptime(photo['upload_date'], "%d %B %Y"),
                                    platform=GPSData.PANORAMIO,
                                    user=photo['owner_name'])
                    data.save()
                    phcount+=1
                    
    return HttpResponse('Finished! saved '+str(phcount))


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
                        #Create local object with the json fields
                        fs_data = FoursquareData(   checkin_count=venue['stats']['checkinsCount'], here_now=venue['hereNow']['count'],
                                                    postal_code=venue['location'].get('postalCode', None), category=venue['categories'][0]['name'],
                                                    venue=venue['name'])
                        fs_data.save()
                        data = GPSData( latitude=venue['location']['lat'], longitude=venue['location']['lng'], date_taken=datetime.datetime.now(), 
                                        platform=GPSData.FOURSQUARE, fs_data=fs_data)
                        data.save()

    return HttpResponse('Finished!\nlast response: </br>'+r.content)

def twitter(request, bbox='8.4931,44.9026,11.4316,46.6381'):
    #url for streaming API limited to the bounding box for Italy
    url = "https://stream.twitter.com/1.1/statuses/filter.json?locations=%s" % (bbox)
    stream = oauth_req(url)
    #Reads the twitter live response
    for  line in stream:
        if line.endswith('\r\n'):
            try:
                 tweet = json.loads(line)
                 #Only saves the gereferenced tweets
                 if tweet.get('coordinates'):
                    tweet_db = TwitterData( latitude=tweet['coordinates']['coordinates'][1], longitude=tweet['coordinates']['coordinates'][0],
                                            user=tweet['user']['screen_name'], date=datetime.datetime.strptime(str(tweet['created_at']), "%a %b %d %H:%M:%S +%f %Y"))
                    if tweet.get('source'):
                        tweet_db.source = tweet['source']
                    if tweet['user'].get('location'):
                        tweet_db.user_location = tweet['user']['location']
                    tweet_db.save()
                    print 'coordinates! ' + str(tweet['coordinates'])
                 else:
                    print tweet
            except:
                print line

        
    return HttpResponse('Finished!\nlast response: </br>'+"<a href='"+str(stream)+"' >"+str(stream)+"</a>")


#Handles twitter oauth and send requests
def oauth_req(url, http_method="GET", post_body="", http_headers=None):
    consumer = oauth.Consumer(key='KEY', secret='CONSUMERSECRET')
    token = oauth.Token(key='TOKENKEY', secret='TOKENSECRET')
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
 
  


