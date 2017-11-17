# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0005_auto_20160704_0055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='image',
        ),
    ]
