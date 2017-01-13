# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0020_auto_20170113_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpsdata',
            name='latitude',
            field=models.DecimalField(default=0.0, max_digits=11, decimal_places=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gpsdata',
            name='longitude',
            field=models.DecimalField(default=0.0, max_digits=11, decimal_places=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='twitterdata',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=7, blank=True),
        ),
        migrations.AlterField(
            model_name='twitterdata',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=7, blank=True),
        ),
    ]
