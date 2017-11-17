from django.db import models
from django.utils.translation import ugettext as _
import soms

class Loading(models.Model):
    ALGORITHM = (
        ('0', _('Algorithm of Reconnection 0')),
        ('1', _('Algorithm of Reconnection 1')),
        ('2', _('Algorithm of Reconnection 2')),
        ('3', _('Algorithm of Reconnection 3')),
        ('4', _('Algorithm of Reconnection 4')),
    )

    MODE = (
        ('0', _('Loading Mode 0')),
        ('1', _('Loading Mode 1')),
        ('2', _('Loading Mode 2')),
        ('3', _('Loading Mode 3')),
    )
    network_map = models.ForeignKey(soms.models.NetworkMap, verbose_name=_('Network map'))
    name = models.CharField(_('Name'), max_length=200)
    steps = models.PositiveIntegerField(_('Steps'))
    algorithm = models.CharField(_('Mode'), max_length=1, choices=ALGORITHM, default=1)
    mode = models.CharField(_('Loading Mode'), max_length=1, choices=MODE, default=1)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _('Loading')
        verbose_name_plural = _('Loading')

class LoadingStat(models.Model):
    step = models.PositiveIntegerField(_('Step'))
    loading = models.ForeignKey(Loading, verbose_name=_('Loading'))
    users = models.TextField(_('Users Stat'))
    disconnect = models.TextField(_('Disconnect Stat'))
    connect = models.TextField(_('Connect Stat'))
    reconnect = models.TextField(_('Reconnect Stat'))
    query = models.TextField(_('Query Stat'))

    connect_count = models.PositiveIntegerField(_('Query count'))
    query_count = models.PositiveIntegerField(_('Query count'))
    disconnect_count = models.PositiveIntegerField(_('Disconnect count'))

    connect_success_count = models.PositiveIntegerField(_('Connect success count'))
    connect_failure_count = models.PositiveIntegerField(_('Connect failure count'))
    reconnect_success_count = models.PositiveIntegerField(_('Reconnect success count'))
    reconnect_failure_count = models.PositiveIntegerField(_('Reconnect failure count'))

class RouteLoadingStat(models.Model):
    step = models.PositiveIntegerField(_('Step'))
    route = models.ForeignKey(soms.models.Route, verbose_name=_('Route'))
    loading = models.ForeignKey(Loading, verbose_name=_('Loading'))
    bandwidth = models.FloatField(_('Bandwidth'))
    users = models.PositiveIntegerField(_('User Count'))

class NodeLoadingStat(models.Model):
    step = models.PositiveIntegerField(_('Step'))
    loading = models.ForeignKey(Loading, verbose_name=_('Loading'))
    node = models.ForeignKey(soms.models.Node, verbose_name=_('Node'))
    input_bandwidth = models.FloatField(_('Input bandwidth'))
    output_bandwidth = models.FloatField(_('Output bandwidth'))
    cpu = models.FloatField(_('CPU'))
    memory = models.FloatField(_('Memory'))
    users = models.PositiveIntegerField(_('User Count'))
    overload = models.FloatField(_('Overload'))

class RouteLoading(models.Model):
    route = models.ForeignKey(soms.models.Route, verbose_name=_('Route'))
    loading = models.ForeignKey(Loading, verbose_name=_('Loading'))
    #bandwidth = models.FloatField(_('Bandwidth'), blank=True, null=True)
    min_bandwidth = models.PositiveIntegerField(_('Minimal Bandwidth'))
    max_bandwidth = models.PositiveIntegerField(_('Maximum Bandwidth'))
    algorithm = models.PositiveIntegerField(_('Algorithm of Distribution'))

    def __unicode__(self):
        return self.route.__unicode__()
    class Meta:
        verbose_name = _('Route Loading')
        verbose_name_plural = _('Route Loadings')
        unique_together = ['route', 'loading']

class UserLoading(models.Model):
    MODE = (
        ('1', _('Add User')),
        ('2', _('Remove User')),
    )

    route = models.ForeignKey(soms.models.Route, verbose_name=_('Route'))
    loading = models.ForeignKey(Loading, verbose_name=_('Loading'))
    user_count = models.PositiveIntegerField(_('User Count'))
    mode = models.CharField(_('Mode'), max_length=1, choices=MODE, default=1)
    step = models.PositiveIntegerField(_('Step Interval'))
    algorithm = models.PositiveIntegerField(_('Algorithm of Connection'))

    def __unicode__(self):
        return str(self.route)
    class Meta:
        verbose_name = _('User Loading')
        verbose_name_plural = _('User Loadings')

class NodeLoading(models.Model):
    node = models.ForeignKey(soms.models.Node, verbose_name=_('Node'))
    loading = models.ForeignKey(Loading, verbose_name=_('Loading'))

    #input_bandwidth = models.FloatField(_('Input bandwidth'))
    min_input_bandwidth = models.PositiveIntegerField(_('Minimal Input Bandwidth'))
    max_input_bandwidth = models.PositiveIntegerField(_('Maximum Input Bandwidth'))
    ib_algorithm = models.PositiveIntegerField(_('Algorithm of Distribution'))

    #output_bandwidth = models.FloatField(_('Output bandwidth'))
    min_output_bandwidth = models.PositiveIntegerField(_('Minimal Output Bandwidth'))
    max_output_bandwidth = models.PositiveIntegerField(_('Maximum Output Bandwidth'))
    ob_algorithm = models.PositiveIntegerField(_('Algorithm of Distribution'))

    #cpu = models.FloatField(_('CPU'))
    min_cpu = models.FloatField(_('Minimal CPU'))
    max_cpu = models.FloatField(_('Maximum CPU'))
    cpu_algorithm = models.PositiveIntegerField(_('Algorithm of Distribution'))

    #memory = models.FloatField(_('Memory'))
    min_memory = models.FloatField(_('Minimal Memory'))
    max_memory = models.FloatField(_('Maximum Memory'))
    memory_algorithm = models.PositiveIntegerField(_('Algorithm of Distribution'))

    def __unicode__(self):
        return self
    class Meta:
        verbose_name = _('Node Loading')
        verbose_name_plural = _('Node Loadings')
        unique_together = ['node', 'loading']
