# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0004_auto_20160114_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='foursquaredata',
            name='radius',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
