# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='thickness',
            field=models.PositiveIntegerField(verbose_name='Thickness', validators=[django.core.validators.MaxValueValidator(10)]),
            preserve_default=True,
        ),
    ]
