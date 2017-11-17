# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0006_remove_node_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='img',
            field=models.ImageField(help_text=b'\xd0\x98\xd0\xb7\xd0\xbe\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x81\xd0\xbe\xd1\x85\xd1\x80\xd0\xb0\xd0\xbd\xd1\x8f\xd1\x8e\xd1\x82\xd1\x81\xd1\x8f \xd0\xb2 /media/images/Node', upload_to=b'images/Node/', null=True, verbose_name=b'\xd0\xa4\xd0\xbe\xd1\x82\xd0\xbe', blank=True),
            preserve_default=True,
        ),
    ]
