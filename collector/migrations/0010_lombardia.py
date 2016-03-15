# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0009_twitterdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lombardia',
            fields=[
                ('gid', models.AutoField(serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=40, null=True, db_column=b'NOME', blank=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'db_table': 'lombardia',
                'managed': False,
            },
        ),
    ]
