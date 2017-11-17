# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from soms.models import NetworkMap, Node, Track, Route, Link
from django.views import generic
from django.views.generic import edit
import json
from django.contrib.admin.widgets import AdminFileWidget
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.forms import *
from django import forms
from django.shortcuts import render_to_response
from django.db.models import Max, Min, Q
from django.db.models import Count
import django
from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.utils.translation import ugettext as _
from django.core.mail import BadHeaderError
from django.contrib import messages
from .forms import FormNetworkMap, FormNetworkMapUpdate, NewNodeForm

def index(request):
    networkmap_list = NetworkMap.objects.select_related().annotate(num_nodes=Count('node'))
    return render(request, 'soms/networkmap_list.html', {'networkmap_list': networkmap_list})

def documents(request):
    return render(request, 'soms/documents/main.html')

def modelka(request):
    netmap = NetworkMap.objects.all()
    node = Node.objects.all()
    track = Track.objects.all()
    return render(request, 'soms/modelka.html', {
        'netmap': netmap, 
        'node': node, 
        'track': track
        })

def main(request):
    return render(request, 'soms/main.html')

class NodeIndex(generic.ListView):
    model = Node

class TrackIndex(generic.ListView):
    model = Track

def AddNetworkMap(request):
    if request.method == 'POST':
        form = FormNetworkMap(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            try:
                return HttpResponseRedirect('/soms/')
            except BadHeaderError:
                return HttpResponse("invalid header error")
    else:
        form = FormNetworkMap()
    return render(request, "soms/networkmap_form.html", {'form': form})


def AddNewNode(request):
    if request.method == 'POST':
        form = NewNodeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            try:
                return HttpResponseRedirect('/soms/')
            except BadHeaderError:
                return HttpResponse("invalid header error")
    else:
        form = NewNodeForm()
    return render(request, "soms/node_add_form_for_model.html", {'form': form})    

class NetworkMapAdd(edit.CreateView):
    model = NetworkMap
    fields = "__all__"
    def get_success_url(self):
        return  reverse_lazy('soms:detail', kwargs={'pk': self.object.id })

class NetworkMapUpdate(edit.UpdateView):
    model = NetworkMap
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return  reverse_lazy('soms:index')

class UpdForm(ModelForm):
    class Meta:
        model = NetworkMap

class UpdFormNet(forms.Form):
    name  = forms.CharField(label=u'Название')
    images = forms.ImageField(label=u'Изображение',required=False)

class NetworkMapUpdateForm(edit.UpdateView):
    model = NetworkMap
    template_name_suffix = '_update_form_for_model'
    def get_success_url(self):
        return  reverse_lazy('soms:detail', kwargs={'pk': self.object.id })

class NetworkMapDelete(edit.DeleteView):
    model = NetworkMap
    def get_success_url(self):
        return  reverse_lazy('soms:index')

class NodeAdd(edit.CreateView):
    model = Node
    fields = "__all__"
    template_name_suffix = '_add_form'
    def get_success_url(self):
        return  reverse_lazy('soms:node:json', kwargs = {'pk':self.object.pk})

class TrackAddForm(ModelForm):
    class Meta:
        model = Track
        fields = "__all__"
    def clean(self):
        super(forms.ModelForm, self).clean()
        start_node = self.cleaned_data.get('start_node', None)
        end_node = self.cleaned_data.get('end_node', None)
        if start_node.id > end_node.id:
            self.cleaned_data['start_node'] = end_node
            self.cleaned_data['end_node'] = start_node
        return self.cleaned_data

class TrackAdd(edit.CreateView):
    form_class = TrackAddForm
    model = Track
    template_name_suffix = '_add_form'
    def get(self, request, *args, **kwargs):
        self.networkmap = get_object_or_404(NetworkMap, pk=self.kwargs['pk'])
        self.object = None
        return super(TrackAdd, self).get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.networkmap = get_object_or_404(NetworkMap, pk=self.kwargs['pk'])
        self.object = None
        return super(TrackAdd, self).post(request, *args, **kwargs)
    def get_form(self, form_class):
        form = super(TrackAdd, self).get_form(form_class)
        if hasattr(self, 'networkmap'):
            form.fields['start_node'].queryset = Node.objects.filter(network_map__exact=self.networkmap)
            form.fields['end_node'].queryset = Node.objects.filter(network_map__exact=self.networkmap)
        return form
    def get_success_url(self):
        return  reverse_lazy('soms:track:json', kwargs = {'pk':self.object.pk})

class LinkAddForm(ModelForm):
    class Meta:
        model = Link
        fields = "__all__"
    def clean(self):
        super(forms.ModelForm, self).clean()
        start_node = self.cleaned_data.get('start_node', None)
        end_node = self.cleaned_data.get('end_node', None)
        if start_node.id > end_node.id:
            self.cleaned_data['start_node'] = end_node
            self.cleaned_data['end_node'] = start_node
        return self.cleaned_data

class LinkAdd(edit.CreateView):
    form_class = LinkAddForm
    model = Link
    template_name_suffix = '_add_form'
    def get(self, request, *args, **kwargs):
        self.networkmap = get_object_or_404(NetworkMap, pk=self.kwargs['pk'])
        self.object = None
        return super(LinkAdd, self).get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.networkmap = get_object_or_404(NetworkMap, pk=self.kwargs['pk'])
        self.object = None
        return super(LinkAdd, self).post(request, *args, **kwargs)
    def get_form(self, form_class):
        form = super(LinkAdd, self).get_form(form_class)
        if hasattr(self, 'networkmap'):
            form.fields['start_node'].queryset = Node.objects.filter(network_map__exact=self.networkmap)
            form.fields['end_node'].queryset = Node.objects.filter(network_map__exact=self.networkmap)
        return form
    def get_success_url(self):
        return  reverse_lazy('soms:link:json', kwargs = {'pk':self.object.pk})

class NodeDelete(edit.DeleteView):
    model = Node
    def get_success_url(self):
        return  reverse_lazy('soms:node:delete_json', kwargs = {'pk':self.object.pk})

class TrackDelete(edit.DeleteView):
    model = Track
    def get_success_url(self):
        return  reverse_lazy('soms:track:delete_json', kwargs = {'pk':self.object.pk})

class LinkDelete(edit.DeleteView):
    model = Link
    def get_success_url(self):
        return  reverse_lazy('soms:link:delete_json', kwargs = {'pk':self.object.pk})

class NodeUpdateForm(ModelForm):
    class Meta:
        model = Node
        exclude = ['network_map', 'x', 'y', 'node_type']

class NodeUpdate(edit.UpdateView):
    model = Node
    form_class = NodeUpdateForm
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return  reverse_lazy('soms:node:json', kwargs = {'pk':self.object.pk})

class TrackUpdateForm(ModelForm):
    class Meta:
        model = Track
        exclude = ['start_node', 'end_node']

class TrackUpdate(edit.UpdateView):
    model = Track
    form_class = TrackUpdateForm
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return  reverse_lazy('soms:track:json', kwargs = {'pk':self.object.pk})

def detail(request, pk):
    networkmap = get_object_or_404(NetworkMap, pk=pk)
    network_map = get_object_or_404(NetworkMap, pk=pk)
    q = Node.objects.filter(network_map=network_map)
    return render(request, 'soms/networkmap_detail.html', {'networkmap': networkmap, 'q': q})

def node_move(request, pk, x, y):
    node = get_object_or_404(Node, pk=pk)
    node.x = x;
    node.y = y;
    node.save()
    return HttpResponse(serializers.serialize('json', [node]),
        content_type='application/json')

def node_json(request, pk):
    node = get_object_or_404(Node, pk=pk)
    return HttpResponse(serializers.serialize('json', [node]),
        content_type='application/json')

def track_json(request, pk):
    track = get_object_or_404(Track, pk=pk)
    return HttpResponse(serializers.serialize('json', [track]), content_type='application/json')

def link_json(request, pk):
    link = get_object_or_404(Link, pk=pk)
    return HttpResponse(serializers.serialize('json', [link]), content_type='application/json')

def node_delete_json(request, pk):
    return HttpResponse(pk,
        content_type='application/json')

def link_delete_json(request, pk):
    return HttpResponse(pk,
        content_type='application/json')

def track_delete_json(request, pk):
    return HttpResponse(pk,
        content_type='application/json')

def route_delete_json(request, pk):
    return HttpResponse(pk,
        content_type='application/json')

def networkmap_node_json(request, pk):
    network_map = get_object_or_404(NetworkMap, pk=pk)
    return HttpResponse(serializers.serialize('json', Node.objects.filter(network_map=network_map)),
        content_type='application/json')

def networkmap_track_json(request, pk):
    network_map = get_object_or_404(NetworkMap, pk=pk)
    return HttpResponse(serializers.serialize('json', Track.objects.filter(start_node__network_map=network_map)),
        content_type='application/json')

def networkmap_link_json(request, pk):
    network_map = get_object_or_404(NetworkMap, pk=pk)
    return HttpResponse(serializers.serialize('json', Link.objects.filter(start_node__network_map=network_map)),
        content_type='application/json')

def networkmap_route_json(request, pk):
    network_map = get_object_or_404(NetworkMap, pk=pk)
    return HttpResponse(serializers.serialize('json', Route.objects.filter(start_node__network_map=network_map)),
        content_type='application/json')

def route_detail(request, pk):
    route = get_object_or_404(Route, pk=pk)
    path = []
    path.append(route.pk)

    while(route.parent):
        path.append(route.parent.pk)
        route = route.parent

    return HttpResponse(json.dumps(path),
        content_type='application/json')


class RouteDeleteForm(forms.Form):
    route = forms.ModelChoiceField(queryset=Route.objects.all(), required=False)

def route_delete(request, pk1, pk2):
    node_from = get_object_or_404(Node, pk=pk1)
    node_to = get_object_or_404(Node, pk=pk2)
    if request.method == 'POST':
        form = RouteDeleteForm(request.POST)
        if(form.is_valid()):
            data = form.cleaned_data
            if data['route']:
                route = data['route']
                pk = route.pk
                route.delete()
                return HttpResponse(pk,
                    content_type='application/json')
    form = RouteDeleteForm()
    form.fields['route'].queryset = Route.objects.filter(Q(start_node=node_from, end_node=node_to) | Q(start_node=node_to, end_node=node_from))
    return render_to_response('soms/route_delete.html',
        {'node_from': node_from, 'node_to': node_to, 'form':form} );

class RouteAddForm(forms.Form):
    name = forms.CharField(label=_('Name'))
    parent = forms.ModelChoiceField(label=_('Parent'), queryset=Route.objects.all(), required=False)
    quality = forms.IntegerField(label=_('Quality'))
    bandwidth = forms.FloatField(label=_('Occupied Bandwidth'))

def route_add(request, pk1, pk2):
    node_from = get_object_or_404(Node, pk=pk1)
    node_to = get_object_or_404(Node, pk=pk2)
    if request.method == 'POST':
        form = RouteAddForm(request.POST)
        if(node_from.node_type == '1' and node_from != node_to):
            form.fields['parent'].required = True

        if(node_from.node_type == '2'):
            form.fields['parent'].required = True
            form.fields['bandwidth'].required = False
            form.fields['quality'].required = False
        if(form.is_valid()):
            data = form.cleaned_data
            bandwidth = data['bandwidth']
            quality = data['quality']
            name = data['name']
            if data['parent'] is None:
                step = 0
            else:
                parent = data['parent']
                step = parent.step + 1
                if(node_from.node_type == '2'):
                    bandwidth = parent.bandwidth
                    quality = parent.quality

                #assert False, locals()
                #if parent.last == True:
                #	parent.last = False
                #	parent.save()

            route = Route.objects.create(
                        name = name,
                        bandwidth = bandwidth,
                        quality = quality,
                        parent = data['parent'],
                        start_node = node_from,
                        end_node = node_to,
                        step = step,
                        )
                        #last = True)
            route.save()
            return HttpResponse(serializers.serialize('json', [route]),
                content_type='application/json')
        else:
            form.fields['parent'].queryset = Route.objects.filter(end_node=node_from)
            if(node_from.node_type == '2'):
                form.fields['bandwidth'].widget.attrs['readonly'] = True
                form.fields['quality'].widget.attrs['readonly'] = True
                form.fields['name'].widget.attrs['readonly'] = True

    else:
        form = RouteAddForm()
        #form.fields['parent'].queryset = Route.objects.filter(Q(end_node__node_type=1, end_node=node_from) | Q(end_node=node_from, last=True))
        form.fields['parent'].queryset = Route.objects.filter(Q(end_node=node_from) & ~Q(start_node=node_to))
        if(node_from.node_type == '2'):
            form.fields['bandwidth'].widget.attrs['readonly'] = True
            form.fields['quality'].widget.attrs['readonly'] = True
            form.fields['name'].widget.attrs['readonly'] = True


    return render_to_response('soms/route_add.html',
        {'node_from': node_from, 'node_to': node_to, 'form':form} );

#форма для ввода названия копии
class NetworkMapCopyForm(forms.Form):
    name = forms.CharField(max_length=200, label=_('Name'))


#функция для копирования модели (принимает параметр (id=pk))
def networkmap_copy(request, pk):
    network_map = get_object_or_404(NetworkMap, pk=pk)
    network_map_pk = network_map.pk
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = NetworkMapCopyForm(request.POST)
            if form.is_valid():
                network_map.name = form.cleaned_data['name']
                network_map.pk = None
                network_map.save()
                pks = {}
                for node in Node.objects.filter(network_map=network_map_pk):
                    pk = node.pk
                    node.pk = None
                    node.network_map = network_map
                    node.save()
                    pks[pk] = node

                for route in Route.objects.filter(start_node__network_map=network_map_pk):
                    route.pk = None
                    route.start_node = pks[route.start_node.pk]
                    route.end_node = pks[route.end_node.pk]
                    route.save()

                for route in Track.objects.filter(start_node__network_map=network_map_pk):
                    route.pk = None
                    route.start_node = pks[route.start_node.pk]
                    route.end_node = pks[route.end_node.pk]
                    route.save()

                for link in Track.objects.filter(start_node__network_map=network_map_pk):
                    route.pk = None
                    route.start_node = pks[route.start_node.pk]
                    route.end_node = pks[route.end_node.pk]
                    route.save()

                return redirect('soms:index')
        else:
            form = NetworkMapCopyForm()
        return render_to_response('soms/networkmap_copy.html', {'form':form, 'networkmap_pk':network_map_pk})
    else:
        return HttpResponse("<h1>You Are Not Authorized to View This Page</h1>")
