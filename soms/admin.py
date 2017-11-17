from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django import forms
from soms.models import NetworkMap, Node, Track, Route

class NodeInline(admin.TabularInline):
    model = Node
    extra = 1

#class TrackInline(admin.TabularInline):
#	model = Track
#	extra = 1

comment = """
    def formfield_for_dbfield(self, field, **kwargs):
        if field.name == 'start_node' or field.name == 'end_node':
            parent_track = self.get_object(kwargs['request'], Track)
            if parent_track:
                nodes = Node.objects.filter(network_map__exact=parent_track.network_map)
                return forms.ModelChoiceField(queryset=nodes)
        return super(StreamInline, self).formfield_for_dbfield(field, **kwargs)

    def get_object(self, request, model):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        try:
            object_id = int(object_id)
        except ValueError:
            return None
        return model.objects.get(pk=object_id)
"""

'''
class NetworkMapAdmin(admin.ModelAdmin):
    inlines = [NodeInline]
'''
class NodeAdmin(admin.ModelAdmin):
    pass

class TrackAdmin(admin.ModelAdmin):
    pass

class RouteAdmin(admin.ModelAdmin):
    #fields = ['name']
    #inlines = [StreamInline]
    #def has_add_permission(self, request):
    #	return False
    pass


admin.site.register(NetworkMap)

admin.site.register(Track, TrackAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Node, NodeAdmin)
