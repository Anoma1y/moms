# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0027_remove_route_color_route'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='thickness_route',
        ),
    ]
