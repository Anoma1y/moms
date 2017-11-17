# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soms', '0015_auto_20160802_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Maket', max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('images', models.ImageField(default=b'https://pp.vk.me/c631127/v631127502/4c484/tuccNy7CBt0.jpg', help_text=b'\xd0\x98\xd0\xb7\xd0\xbe\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x81\xd0\xbe\xd1\x85\xd1\x80\xd0\xb0\xd0\xbd\xd1\x8f\xd1\x8e\xd1\x82\xd1\x81\xd1\x8f \xd0\xb2 /media/images/Photo', verbose_name=b'\xd0\xa4\xd0\xbe\xd1\x82\xd0\xbe', upload_to=b'images/Photo/')),
            ],
            options={
                'verbose_name': 'Maket map',
                'verbose_name_plural': 'Maket maps',
            },
            bases=(models.Model,),
        ),
    ]
