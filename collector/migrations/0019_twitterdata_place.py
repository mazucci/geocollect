# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0018_auto_20161006_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterdata',
            name='place',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
