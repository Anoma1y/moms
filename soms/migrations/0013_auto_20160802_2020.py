# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0012_auto_20160730_2053'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NetworkMapUnregistered',
        ),
        migrations.AlterField(
            model_name='node',
            name='color',
            field=colorfield.fields.ColorField(default=b'#000000', max_length=10, verbose_name='Color'),
            preserve_default=True,
        ),
    ]
