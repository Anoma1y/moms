# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0024_auto_20170416_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='thickness',
            field=models.PositiveIntegerField(verbose_name='Thickness', validators=[django.core.validators.MaxValueValidator(5)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='track',
            name='thickness',
            field=models.PositiveIntegerField(verbose_name='Thickness', validators=[django.core.validators.MaxValueValidator(5)]),
            preserve_default=True,
        ),
    ]
