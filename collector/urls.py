from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^flickr/', 'collector.views.flickr', name='flickr'),
    url(r'^panoramio/', 'collector.views.panoramio', name='panoramio'),
    url(r'^foursquare/$', 'collector.views.foursquare_circle', name='4square'),
    url(r'^foursquare/(?P<user>\w+)/$', 'collector.views.foursquare_circle', name='4square_user'),
    url(r'^twitter/$', 'collector.views.twitter', name='twitter'),
    url(r'^twitter/(?P<bbox>(-?\d+\.\d+,-?\d+\.\d+,-?\d+\.\d+,-?\d+\.\d+))/$', 'collector.views.twitter', name='twitter_bbox'),
    url(r'^json/(?P<platform>\w+)/((?P<date_start>(\w|\-|\:)+)/)?((?P<date_end>(\w|\-|\:)+)/)?((?P<keyword>[\w &]+)/)?$', 'collector.views.json_OL_heatmap', name='json'),

]