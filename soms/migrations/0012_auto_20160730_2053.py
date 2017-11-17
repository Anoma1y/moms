# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0011_auto_20160727_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='ip',
            field=models.IPAddressField(verbose_name='IP-\u0430\u0434\u0440\u0435\u0441'),
            preserve_default=True,
        ),
    ]
