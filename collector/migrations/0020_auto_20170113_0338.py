# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0019_twitterdata_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpsdata',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=7, blank=True),
        ),
        migrations.AlterField(
            model_name='gpsdata',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=7, blank=True),
        ),
    ]
