import time
from django.db import models
from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point

# Create your models here.

class GPSData(models.Model):
    FLICKR = 'FLC'
    PANORAMIO = 'PNR'
    FOURSQUARE = 'FSQ'
    PLATFORM_CHOICES = (
        (FLICKR, 'Flickr'),
        (PANORAMIO, 'Panoramio'),
        (FOURSQUARE, 'FSQ'),
    )

    latitude = models.DecimalField(max_digits=11, decimal_places=7)
    longitude = models.DecimalField(max_digits=11, decimal_places=7)
    date_taken = models.DateTimeField(null=True, blank=True, db_index=True)
    date_posted = models.DateTimeField(null=True, blank=True)
    user = models.CharField(max_length=200, null=True, blank=True)
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES, default=FLICKR)
    fs_data = models.ForeignKey('FoursquareData', null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, blank=True, null=True)
    fs_dup = models.BooleanField(default=False)
    p_geom = geo_models.GeometryField()
    lombardy = models.IntegerField(blank=True, null=True)
    local_id = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        ordering = ['-date_taken']
        verbose_name = 'GPS Data'
        verbose_name_plural = "GPS Data"

    def __unicode__(self):
        return "LAT: " + str(self.latitude) + " LON: " + str(self.longitude) + " - " + str(self.date_taken) + " | " + self.platform

    @classmethod
    def del_dups(cls):
        c = 0
        for row in cls.objects.filter(platform='FSQ', fs_dup=False):
            #Same location, day/hour and venue > 1?  Delete!
            if cls.objects.filter(latitude=row.latitude, longitude=row.longitude,
                                  date_taken__day=row.date_taken.day, date_taken__month=row.date_taken.month,
                                  date_taken__year=row.date_taken.year, date_taken__hour=row.date_taken.hour,
                                  fs_data__venue=row.fs_data.venue).count() > 1:
                row.fs_data.delete()
                row.delete()
                c += 1
                print "deleted %s" % c
        print 'deleted FSQ: ' +str(c)

        c=0
        for row in cls.objects.filter(platform='FLC'):
            #Same location, day/hour and user > 1?  Delete!
            if cls.objects.filter(latitude=row.latitude, longitude=row.longitude, user=row.user,
                                  date_taken=row.date_taken, date_posted=row.date_posted,
                                  local_id=row.local_id).count() > 1:
                row.delete()
                c += 1
        print 'deleted FLC: ' +str(c)


    @property
    def point(self):
        return Point(self.longitude, self.latitude, srid=4326)

    @classmethod
    def gen_fs_dups(cls):
        added = 0
        #Delete previously created dups
        cls.objects.filter(platform='FSQ', fs_dup=True).delete()
        #Look for originals
        for row in cls.objects.filter(platform='FSQ', fs_dup=False):
            #More than 1 checkin?
            if row.fs_data.here_now > 1:
                #Create duplicate for each checkin
                for i in range(row.fs_data.here_now-1):
                    new = row
                    new.pk = None
                    new.fs_dup = True
                    new.save()
                    added += 1
        print "Total added: %s" % added



class FoursquareData(models.Model):
    checkin_count = models.IntegerField(null=True, blank=True)
    here_now = models.IntegerField(null=True, blank=True)
    user_count = models.IntegerField(null=True, blank=True)
    venue = models.CharField(max_length=500)
    postal_code = models.CharField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=250, null=True, blank=True)
    radius = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "Venue: " + self.venue 

class FSCircle(models.Model):
    latitude = models.DecimalField(max_digits=11, decimal_places=7)
    longitude = models.DecimalField(max_digits=11, decimal_places=7)
    radius = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "Radius: " + self.radius

class TwitterData(models.Model):
    latitude = models.DecimalField(max_digits=11, decimal_places=7)
    longitude = models.DecimalField(max_digits=11, decimal_places=7)
    date = models.DateTimeField(null=True, blank=True, db_index=True)
    source = models.CharField(max_length=250, null=True, blank=True)
    user = models.CharField(max_length=300, null=True)
    user_location = models.CharField(max_length=300, null=True, blank=True)
    text = models.CharField(max_length=200, null=True)
    hashtags = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return "User: " + self.user + "  LatLon: " + str(self.latitude) + ", " + str(self.longitude)

    @classmethod
    def del_dups(cls):
        _all = TwitterData.objects.exclude(text__isnull=True, text__exact="")
        for row in _all:
            if cls.objects.filter(user=row.user, latitude=row.latitude, longitude=row.longitude,
                                  date=row.date, text=row.text).count() > 1:
                row.delete()

class Lombardia(models.Model):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(db_column='NOME', max_length=40, blank=True, null=True)  # Field name made lowercase.
    geom = geo_models.MultiPolygonField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lombardia'

    @classmethod
    def get_lomb(cls):
        return cls.objects.filter()[0].geom