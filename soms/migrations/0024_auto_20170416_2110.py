# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0023_auto_20170416_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='color',
            field=colorfield.fields.ColorField(default=3, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='track',
            name='thickness',
            field=models.PositiveIntegerField(default=1, verbose_name='Thickness', validators=[django.core.validators.MaxValueValidator(10)]),
            preserve_default=False,
        ),
    ]
