# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0013_auto_20160802_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='color',
            field=colorfield.fields.ColorField(max_length=10, verbose_name='Color'),
            preserve_default=True,
        ),
    ]
