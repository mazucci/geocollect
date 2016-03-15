# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0010_lombardia'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpsdata',
            name='fs_dup',
            field=models.BooleanField(default=False),
        ),
    ]
