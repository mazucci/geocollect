# geocollect
Scripts for collecting georeferenced data from Twitter, Flickr, Foursquare and Panoramio by the GEOLab - Laboratorio di Geomatica e Osservazione della Terra, used for the ISPRS 2016 Conference: "Sensing slow mobility and interesting locations for Lombardy Region (Italy): a case study using pointwise geolocated open data"

Django 1.8 project to store in a potgres+postgis database georenferenced data using Twitter, Flickr, Foursquare and Panoramio APIs

Requirements
-------------

    * Django 1.8 (https://github.com/django/django/tree/stable/1.8.x)
    * postgres + postgis (http://www.postgresql.org/download/)
    * requests (http://docs.python-requests.org/en/master/)
    * oauth2 (https://github.com/joestump/python-oauth2)
    * flickrapi (https://pypi.python.org/pypi/flickrapi)
