# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0020_auto_20170305_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmap',
            name='imgHeight',
            field=models.IntegerField(max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='networkmap',
            name='imgWidth',
            field=models.IntegerField(max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='networkmap',
            name='imgX',
            field=models.IntegerField(max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='networkmap',
            name='imgY',
            field=models.IntegerField(max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
