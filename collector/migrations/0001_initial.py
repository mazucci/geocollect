# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GPSData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(max_digits=11, decimal_places=7)),
                ('longitude', models.DecimalField(max_digits=11, decimal_places=7)),
                ('date_taken', models.DateTimeField()),
                ('date_posted', models.DateTimeField()),
                ('user', models.CharField(max_length=200)),
                ('platform', models.CharField(default=b'FLC', max_length=10, choices=[(b'FLC', b'Flickr'), (b'PNR', b'Panoramio')])),
            ],
            options={
                'ordering': ['date_taken'],
                'verbose_name': 'GPS Data',
                'verbose_name_plural': 'GPS Datas',
            },
        ),
    ]
