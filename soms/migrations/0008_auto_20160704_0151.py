# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0007_node_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='img',
        ),
        migrations.AddField(
            model_name='node',
            name='image',
            field=models.CharField(blank=True, max_length=250, null=True, choices=[(b'images/Node/node_image/first.png', b'Facebook')]),
            preserve_default=True,
        ),
    ]
