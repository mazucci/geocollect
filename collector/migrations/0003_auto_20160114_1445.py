# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0002_auto_20160112_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoursquareData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('checkin_count', models.IntegerField(null=True, blank=True)),
                ('here_now', models.IntegerField(null=True, blank=True)),
                ('user_count', models.IntegerField(null=True, blank=True)),
                ('venue', models.CharField(max_length=500)),
                ('postal_code', models.IntegerField(null=True, blank=True)),
                ('category', models.CharField(max_length=250, null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='gpsdata',
            name='platform',
            field=models.CharField(default=b'FLC', max_length=10, choices=[(b'FLC', b'Flickr'), (b'PNR', b'Panoramio'), (b'FSQ', b'FSQ')]),
        ),
        migrations.AddField(
            model_name='gpsdata',
            name='FS_data',
            field=models.ForeignKey(to='collector.FoursquareData', null=True),
        ),
    ]
