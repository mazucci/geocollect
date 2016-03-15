# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0003_auto_20160114_1445'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gpsdata',
            old_name='FS_data',
            new_name='fs_data',
        ),
        migrations.AlterField(
            model_name='gpsdata',
            name='date_posted',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='gpsdata',
            name='user',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
