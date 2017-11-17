# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0008_auto_20160704_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='image',
            field=models.CharField(blank=True, max_length=250, null=True, choices=[(b'first.png', b'Facebook')]),
            preserve_default=True,
        ),
    ]
