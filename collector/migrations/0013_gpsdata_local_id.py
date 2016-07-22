# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0012_auto_20160304_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpsdata',
            name='local_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
