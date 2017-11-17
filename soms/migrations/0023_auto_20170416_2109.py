# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0022_auto_20170414_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='color',
            field=colorfield.fields.ColorField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='thickness',
            field=models.PositiveIntegerField(default=3, verbose_name='Thickness', validators=[django.core.validators.MaxValueValidator(10)]),
            preserve_default=False,
        ),
    ]
