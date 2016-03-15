# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0006_fscircle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foursquaredata',
            name='postal_code',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
