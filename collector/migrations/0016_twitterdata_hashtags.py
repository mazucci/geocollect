# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0015_twitterdata_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterdata',
            name='hashtags',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
