# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0005_foursquaredata_radius'),
    ]

    operations = [
        migrations.CreateModel(
            name='FSCircle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(max_digits=11, decimal_places=7)),
                ('longitude', models.DecimalField(max_digits=11, decimal_places=7)),
                ('radius', models.IntegerField(null=True, blank=True)),
            ],
        ),
    ]
