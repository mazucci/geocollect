# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0014_auto_20160318_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterdata',
            name='text',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
