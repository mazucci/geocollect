# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0013_gpsdata_local_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpsdata',
            name='local_id',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
    ]
