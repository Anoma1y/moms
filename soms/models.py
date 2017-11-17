# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator
# Create your models here.

class NetworkMap(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    images = models.ImageField("Фото", upload_to="images/Photo/",
                            help_text="Изображения сохраняются в /media/images/Photo", blank=True)
    imgX = models.CharField(max_length=20, blank=True)
    imgY = models.CharField(max_length=20, blank=True)
    imgWidth = models.CharField(max_length=20, blank=True)
    imgHeight = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _('Network map')
        verbose_name_plural = _('Network maps')

class Node(models.Model):
    NODETYPE = (
        ('1', _('Replicator')),
        ('2', _('Reflector')),
        ('3', _('IP Node')),
    )
    NODEIMAGE = (
        ('first.png', 'Facebook'),
        ('computer.png', 'Computer'),
        ('server.png', 'Server'),
        ('bd.png', 'Database'),
    )
    network_map = models.ForeignKey(NetworkMap, verbose_name=_('Network map'))
    name = models.CharField(_('Name'), max_length=200)
    node_type = models.CharField(_('Type'), max_length=1, choices=NODETYPE)
    control_manager = models.BooleanField(_('Control manager'), default=False)
    ip = models.IPAddressField(_('IP address')) #IPAddressField
    max_users = models.PositiveIntegerField(_('Maximum of users'))
    output_bandwidth = models.FloatField(_('Output bandwidth'))
    input_bandwidth = models.FloatField(_('Input bandwidth'))
    cpu = models.FloatField(_('CPU'))
    memory = models.FloatField(_('Memory'))
    thickness = models.PositiveIntegerField(_('Thickness'), validators=[MaxValueValidator(10)])
    color = ColorField(_('Color'))
    popularity = models.PositiveIntegerField(_('Popularity'))
    image = models.CharField(max_length=250, blank=True, null=True, choices=NODEIMAGE)
    x = models.IntegerField()
    y = models.IntegerField()
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _('Node')
        verbose_name_plural = _('Nodes')
        unique_together = [['network_map', 'ip'], ['network_map', 'name']]

class Track(models.Model):
    start_node	= models.ForeignKey(Node, related_name='start_tracks', verbose_name=_('Start node'))
    end_node	= models.ForeignKey(Node, related_name='end_tracks', verbose_name=_('End node'))
    bandwidth = models.FloatField(_('Bandwidth'))
    thickness_track = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    color_track = ColorField()
    def __unicode__(self):
        return self.start_node.name + " - " + self.end_node.name
    class Meta:
        verbose_name = _('Track')
        verbose_name_plural = _('Tracks')
        unique_together = ['start_node', 'end_node']

class Route(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    bandwidth = models.FloatField(_('Bandwidth'))
    quality = models.PositiveIntegerField(_('Quality'))
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name=_('Parent'))
    start_node	= models.ForeignKey(Node, related_name='start_routes', verbose_name=_('Start node'))
    end_node	= models.ForeignKey(Node, related_name='end_routes', verbose_name=_('End node'))
    step = models.PositiveIntegerField(_('Step'))
    def __unicode__(self):
        if(self.start_node.name == self.end_node.name): return self.name + " (" + self.start_node.name + ") " + str(self.bandwidth)
        else: return self.name + " (" + self.start_node.name + " - " + self.end_node.name + ") " + str(self.bandwidth)
    class Meta:
        verbose_name = _('Route')
        verbose_name_plural = _('Routes')


class Link(models.Model):
    start_node	= models.ForeignKey(Node, related_name='start_links', verbose_name=_('Start node'))
    end_node	= models.ForeignKey(Node, related_name='end_links', verbose_name=_('End node'))
    def __unicode__(self):
        return self.start_node.name + " - " + self.end_node.name
    class Meta:
        verbose_name = _('Control Manager Link')
        verbose_name_plural = _('Control Manager Links')
        unique_together = ['start_node', 'end_node']

