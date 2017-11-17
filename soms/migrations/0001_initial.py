# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Control Manager Link',
                'verbose_name_plural': 'Control Manager Links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NetworkMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('images', models.ImageField(help_text=b'\xd0\x98\xd0\xb7\xd0\xbe\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x81\xd0\xbe\xd1\x85\xd1\x80\xd0\xb0\xd0\xbd\xd1\x8f\xd1\x8e\xd1\x82\xd1\x81\xd1\x8f \xd0\xb2 /media/images/Photo', upload_to=b'images/Photo/', verbose_name=b'\xd0\xa4\xd0\xbe\xd1\x82\xd0\xbe')),
            ],
            options={
                'verbose_name': '\u041c\u043e\u0434\u0435\u043b\u044c',
                'verbose_name_plural': '\u041c\u043e\u0434\u0435\u043b\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('node_type', models.CharField(max_length=1, verbose_name='\u0422\u0438\u043f', choices=[(b'1', '\u0420\u0435\u043f\u043b\u0438\u043a\u0430\u0442\u043e\u0440'), (b'2', '\u0420\u0435\u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0442\u043e\u0440'), (b'3', '\u0423\u0437\u0435\u043b')])),
                ('control_manager', models.BooleanField(default=False, verbose_name='\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440 \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u044f')),
                ('ip', models.IPAddressField(verbose_name='IP-\u0430\u0434\u0440\u0435\u0441')),
                ('max_users', models.PositiveIntegerField(verbose_name='\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439')),
                ('output_bandwidth', models.FloatField(verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u0438\u0441\u0445\u043e\u0434\u044f\u0449\u0435\u0433\u043e \u043a\u0430\u043d\u0430\u043b\u0430 (\u041c\u0431\u0438\u0442)')),
                ('input_bandwidth', models.FloatField(verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u0432\u0445\u043e\u0434\u044f\u0449\u0435\u0433\u043e \u043a\u0430\u043d\u0430\u043b\u0430 (\u041c\u0431\u0438\u0442)')),
                ('cpu', models.FloatField(verbose_name='\u041e\u0431\u044a\u0451\u043c \u0440\u0435\u0441\u0443\u0440\u043e\u0441\u0432 \u043f\u0440\u043e\u0446\u0435\u0441\u0441\u043e\u0440\u0430')),
                ('memory', models.FloatField(verbose_name='\u041e\u0431\u044a\u0451\u043c \u043f\u0430\u043c\u044f\u0442\u0438')),
                ('thickness', models.PositiveIntegerField(verbose_name='Thickness')),
                ('color', colorfield.fields.ColorField(max_length=10, verbose_name='Color')),
                ('popularity', models.PositiveIntegerField(verbose_name='\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u043e\u0441\u0442\u044c')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('network_map', models.ForeignKey(verbose_name='\u041c\u043e\u0434\u0435\u043b\u044c', to='soms.NetworkMap')),
            ],
            options={
                'verbose_name': '\u0423\u0437\u0435\u043b',
                'verbose_name_plural': '\u0423\u0437\u043b\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('bandwidth', models.FloatField(verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u043a\u0430\u043d\u0430\u043b\u0430 (\u041c\u0431\u0438\u0442)')),
                ('quality', models.PositiveIntegerField(verbose_name='\u041a\u0430\u0447\u0435\u0441\u0442\u0432\u043e')),
                ('step', models.PositiveIntegerField(verbose_name='\u0428\u0430\u0433')),
                ('end_node', models.ForeignKey(related_name='end_routes', verbose_name='\u041a\u043e\u043d\u0435\u0447\u043d\u044b\u0439 \u0443\u0437\u0435\u043b', to='soms.Node')),
                ('parent', models.ForeignKey(verbose_name='\u041f\u043e\u0442\u043e\u043a-\u0440\u043e\u0434\u0438\u0442\u0435\u043b\u044c', blank=True, to='soms.Route', null=True)),
                ('start_node', models.ForeignKey(related_name='start_routes', verbose_name='\u041d\u0430\u0447\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0437\u0435\u043b', to='soms.Node')),
            ],
            options={
                'verbose_name': '\u0412\u0435\u0442\u043a\u0430 \u0432 \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u0435',
                'verbose_name_plural': '\u0412\u0435\u0442\u043a\u0438 \u0432 \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u0435',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bandwidth', models.FloatField(verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u043a\u0430\u043d\u0430\u043b\u0430 (\u041c\u0431\u0438\u0442)')),
                ('end_node', models.ForeignKey(related_name='end_tracks', verbose_name='\u041a\u043e\u043d\u0435\u0447\u043d\u044b\u0439 \u0443\u0437\u0435\u043b', to='soms.Node')),
                ('start_node', models.ForeignKey(related_name='start_tracks', verbose_name='\u041d\u0430\u0447\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0437\u0435\u043b', to='soms.Node')),
            ],
            options={
                'verbose_name': '\u0421\u0432\u044f\u0437\u044c \u0432 \u0442\u043e\u043f\u043e\u043b\u043e\u0433\u0438\u0438',
                'verbose_name_plural': '\u0421\u0432\u044f\u0437\u0438 \u0432 \u0442\u043e\u043f\u043e\u043b\u043e\u0433\u0438\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='track',
            unique_together=set([('start_node', 'end_node')]),
        ),
        migrations.AlterUniqueTogether(
            name='node',
            unique_together=set([('network_map', 'name'), ('network_map', 'ip')]),
        ),
        migrations.AddField(
            model_name='link',
            name='end_node',
            field=models.ForeignKey(related_name='end_links', verbose_name='\u041a\u043e\u043d\u0435\u0447\u043d\u044b\u0439 \u0443\u0437\u0435\u043b', to='soms.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='start_node',
            field=models.ForeignKey(related_name='start_links', verbose_name='\u041d\u0430\u0447\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0437\u0435\u043b', to='soms.Node'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together=set([('start_node', 'end_node')]),
        ),
    ]
