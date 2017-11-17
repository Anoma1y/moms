# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0025_auto_20170417_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='route',
            old_name='color',
            new_name='color_route',
        ),
        migrations.RenameField(
            model_name='track',
            old_name='color',
            new_name='color_track',
        ),
        migrations.RemoveField(
            model_name='route',
            name='thickness',
        ),
        migrations.RemoveField(
            model_name='track',
            name='thickness',
        ),
        migrations.AddField(
            model_name='route',
            name='thickness_route',
            field=models.PositiveIntegerField(default=3, validators=[django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='track',
            name='thickness_track',
            field=models.PositiveIntegerField(default=2, validators=[django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
    ]
