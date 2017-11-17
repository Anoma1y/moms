# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0018_auto_20170202_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkmap',
            name='imgHeight',
            field=models.CharField(default=3, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='networkmap',
            name='imgWidth',
            field=models.CharField(default=4, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='networkmap',
            name='imgX',
            field=models.CharField(default=5, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='networkmap',
            name='imgY',
            field=models.CharField(default=5, max_length=20),
            preserve_default=False,
        ),
    ]
