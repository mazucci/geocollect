# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gpsdata',
            options={'ordering': ['date_taken'], 'verbose_name': 'GPS Data', 'verbose_name_plural': 'GPS Data'},
        ),
        migrations.AlterField(
            model_name='gpsdata',
            name='date_taken',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
