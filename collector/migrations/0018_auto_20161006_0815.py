# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0017_twitterdata_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gpsdata',
            options={'ordering': ['-date_taken'], 'verbose_name': 'GPS Data', 'verbose_name_plural': 'GPS Data'},
        ),
        migrations.AlterModelOptions(
            name='twitterdata',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='gpsdata',
            name='date_taken',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='twitterdata',
            name='date',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
        ),
    ]
