# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0016_twitterdata_hashtags'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterdata',
            name='country',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
