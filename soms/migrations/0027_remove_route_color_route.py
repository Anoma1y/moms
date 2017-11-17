# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0026_auto_20170417_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='color_route',
        ),
    ]
