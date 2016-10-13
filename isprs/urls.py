from django.conf.urls import include, url
from django.contrib import admin
from collector.views import heatmap

urlpatterns = [
    # Examples:
    url(r'^$', heatmap, name='heatmap'),
    url(r'^collector/', include('collector.urls')),

    url(r'^admin/', include(admin.site.urls)),


]
