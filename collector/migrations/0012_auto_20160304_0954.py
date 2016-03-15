# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0011_gpsdata_fs_dup'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpsdata',
            name='lombardy',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='gpsdata',
            name='p_geom',
            field=django.contrib.gis.db.models.fields.GeometryField(default='', srid=4326),
            preserve_default=False,
        ),
    ]
