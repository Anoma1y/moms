#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.generic import edit
from soms.models import NetworkMap, Node, Route
from loms.models import Loading, UserLoading, RouteLoading, NodeLoading, NodeLoadingStat, RouteLoadingStat, LoadingStat
from loms import aod, aoc, aor
from django.db.models import F
from django.db.models import *

from django.core.urlresolvers import reverse_lazy
from django import forms
from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.db.models import Max, Min, Q, Sum
from django.shortcuts import render_to_response
from django.core import serializers
from django.forms.models import modelformset_factory
import time

def index(request):
    loading_list = Loading.objects.all()
    return render(request, 'loms/loading_list.html', {'loading_list': loading_list})

def detail(request, pk):
    loading = get_object_or_404(Loading, pk=pk)
    networkmap = loading.network_map
    return render(request, 'loms/loading_detail.html',
        {'loading': loading, 'networkmap': networkmap })

def node_chart(request, pk, node_pk):
    loading = get_object_or_404(Loading, pk=pk)
    node = get_object_or_404(Node, pk=node_pk)
    node_stat = NodeLoadingStat.objects.filter(loading=loading, node=node)
    return render(request, 'loms/node_chart.html',
        {'node':node, 'loading': loading, 'node_stat': node_stat })

def route_chart(request, pk, route_pk):
    loading = get_object_or_404(Loading, pk=pk)
    route = get_object_or_404(Route, pk=route_pk)
    network_map = loading.network_map

    for stream in Route.objects.filter(start_node__network_map=network_map):
        aor.add_stream(stream)

    route_stat = []
    for i in xrange(1, loading.steps + 1):
        route_loading_stat = RouteLoadingStat.objects.filter(loading=loading, step=i)
        users = 0
        for stat in route_loading_stat:
            if aor.check_relation(route.pk, stat.route.pk):
                users += stat.users
        route_stat.append({'step':i, 'users': users})

    return render(request, 'loms/route_chart.html',
        {'route':route, 'loading': loading, 'route_stat': route_stat })

def route_list_chart(request, pk):
    loading = get_object_or_404(Loading, pk=pk)
    network_map = loading.network_map
    routes = Route.objects.filter(start_node__network_map=network_map, start_node=F("end_node"))
    return render(request, 'loms/route_list_chart.html',
        {'loading': loading, 'routes': routes })

def node_list_chart(request, pk):
    loading = get_object_or_404(Loading, pk=pk)
    network_map = loading.network_map
    nodes = Node.objects.filter(network_map=network_map)
    return render(request, 'loms/node_list_chart.html',
        {'loading': loading, 'nodes': nodes })

def loading_chart(request, pk):
    loading = get_object_or_404(Loading, pk=pk)
    loading_stat = LoadingStat.objects.filter(loading=loading)
    return render(request, 'loms/loading_chart.html',
        {'loading': loading, 'loading_stat': loading_stat })

def user_stat(request, pk):
    loading = get_object_or_404(Loading, pk=pk)

    if LoadingStat.objects.filter(loading=loading).count() > 0:
        loading_stat = LoadingStat.objects.filter(loading=loading)
        routes_stat = RouteLoadingStat.objects.filter(loading=loading)
        nodes_stat = NodeLoadingStat.objects.filter(loading=loading)
        stat = LoadingStat.objects.filter(loading=loading).aggregate(Sum('connect_count'), Sum('disconnect_count'), Sum('connect_success_count'), Sum('reconnect_success_count'))
        stat['success'] = stat['connect_success_count__sum'] + stat['reconnect_success_count__sum']
        stat['failure'] = stat['connect_count__sum'] - stat['success']
        return render(request, 'loms/user_stat.html',
            {'loading': loading, 'loading_stat': loading_stat, 'routes_stat': routes_stat, 'nodes_stat': nodes_stat, 'stat': stat })

    start_time = time.time()

    points = {}
    aor.streams = {}
    nodes = Node.objects.filter(network_map=loading.network_map)
    for node in nodes:
        points[node.pk] = node
        node.streams = {}
        node.user_count = 0
        node_loadings = NodeLoading.objects.filter(loading=loading, node=node)
        if len(node_loadings) > 0:
            node.loading =  node_loadings[0]
        else: node.loading = False

        node.overload = node.output_bandwidth
        node.overload2 = node.input_bandwidth
        if node.loading:
            node.overload -= node.output_bandwidth * node.loading.max_output_bandwidth / 100

        for route in node.start_routes.exclude(start_node=F("end_node")):
            node.overload -= route.bandwidth

        for route in node.end_routes.exclude(start_node=F("end_node")):
            node.overload2 -= route.bandwidth

        for route in node.start_routes.filter(start_node=F("end_node")):
            route_loadings = RouteLoading.objects.filter(loading=loading, route=route)
            if len(route_loadings) > 0:
                route.loading =  route_loadings[0]
            else: route.loading = False
            route.node = node
            route.user_count = 0
            route.users = []
            route.brandwidth = route.bandwidth
            aor.add_stream(route)
            aor.add_stream_to_point(route, node)
        for route in node.end_routes.exclude(start_node=F("end_node")):
            route_loadings = RouteLoading.objects.filter(loading=loading, route=route)
            if len(route_loadings) > 0:
                route.loading =  route_loadings[0]
            else: route.loading = False
            route.node = node
            route.user_count = 0
            route.users = []
            route.brandwidth = route.bandwidth
            aor.add_stream(route)
            aor.add_stream_to_point(route, node)



    user_adds = UserLoading.objects.filter(loading=loading, mode="1")
    user_dels = UserLoading.objects.filter(loading=loading, mode="2")

    add_query = []
    del_query = []

    for step in xrange(1, loading.steps + 1):
        print "Шаг %i из %i" % (step, loading.steps)

        stat = LoadingStat()
        stat.step = step
        stat.loading = loading

        users_stat = []
        disconnect_stat = []
        connect_stat = []
        reconnect_stat = []
        reconnect_log = []
        query_stat = []

        connect_count = 0
        query_count = 0
        disconnect_count = 0
        connect_success_count = 0
        connect_failure_count = 0
        reconnect_success_count = 0
        reconnect_failure_count = 0

        query_count = len(add_query)

        for user_add in user_adds:
            if step % user_add.step == 0:
                users_stat.append({'route': user_add.route.id, 'algorithm': user_add.algorithm, 'count': user_add.user_count})
                for i in xrange(user_add.user_count):
                    connect_count += 1
                    add_query.append({'route': user_add.route, 'step': step, 'algorithm': user_add.algorithm})
        for user_del in user_dels:
            if step % user_del.step == 0:
                for i in xrange(user_del.user_count):
                    del_query.append({'route': user_del.route, 'step': user_del.step, 'algorithm': user_del.algorithm})
        if len(del_query):
            pointer = 0
            while 1:
                if len(del_query) == 0: break
                func = aoc.get_function(del_query[pointer]['algorithm'])
                stream = func(points, del_query[0]['route'], 2)
                if stream:
                    aor.stream_del_user(stream)
                    disconnect_stat.append({'route':del_query[0]['route'].id, 'stream':stream.pk})

                    disconnect_count += 1
                del del_query[0]

        if len(add_query):
            pointer = 0
            while 1:
                if len(add_query) == 0 or pointer == len(add_query): break
                func = aoc.get_function(add_query[pointer]['algorithm'])
                stream = func(points, add_query[pointer]['route'], 1)
                if stream == False:
                    pointer += 1
                    connect_failure_count += 1
                    continue
                elif stream.node.overload - stream.brandwidth < 0:
                    connect_failure_count += 1

                    if loading.algorithm == '0':
                        pointer += 1
                        continue

                    aor.stream_add_user(stream)
                    answer = False
                    if loading.algorithm == '1':
                        answer = aor.clean(points, [stream.node.id], larger=False)
                    elif loading.algorithm == '2':
                        answer = aor.clean(points, [stream.node.id])
                    elif loading.algorithm == '3':
                        answer = aor.clear_with_decrease(points, stream.node.id, larger=False)
                    elif loading.algorithm == '4':
                        answer = aor.clear_with_decrease(points, stream.node.id)

                    if answer:
                        points = answer[0]
                        reconnect_success_count += 1
                        reconnect_stat.append({'route':add_query[pointer]['route'].id, 'stream':stream.pk})
                        reconnect_log.append(answer[1:])

                        for point_id in points:
                            for stream_id in points[point_id].streams:
                                aor.add_stream(points[point_id].streams[stream_id])
                        del add_query[0]
                        continue
                    else:
                        aor.stream_del_user(stream)
                        reconnect_failure_count += 1
                        pointer += 1
                        continue
                connect_success_count += 1
                connect_stat.append({'route':add_query[pointer]['route'].id, 'stream':stream.pk})
                aor.stream_add_user(stream)
                del add_query[0]

        for query in add_query:
            query_stat.append({'route': query['route'].id, 'step': query['step'], 'algorithm': query['algorithm']})


        stat.disconnect = disconnect_stat

        if len(disconnect_stat):
            output = "<div><span class='show'>Количество заявок: %s</span><div class='frame'>" % (len(disconnect_stat))
            for s in disconnect_stat:
                output += "Поток:%s<br />" % (aor.streams[s['stream']])
            output += "</div></div>"
            stat.disconnect = output
        else: stat.disconnect = "&nbsp;"

        if len(users_stat):
            output = "<div><span class='show'>Количество заявок: %s</span><div class='frame'>" % (len(users_stat))
            for s in users_stat:
                output += "Поток:%s, количество заявок:%s, алгоритм подключения:%s<br />" % (aor.streams[s['route']], s['count'], s['algorithm'])
            output += "</div></div>"
            stat.users = output
        else: stat.users = "&nbsp;"

        if len(connect_stat):
            output = "<div><span class='show'>Успешных подключений: %s</span><div class='frame'>" % (len(connect_stat))
            for s in connect_stat:
                output += "Заявка на подключение к потоку:%s, подключил к:%s<br />" % (aor.streams[s['route']], aor.streams[s['stream']])
            output += "</div></div>"
            stat.connect = output
        else: stat.connect = "&nbsp;"

        if len(reconnect_stat):
            output = "<div><span class='show'>Успешных подключений с переподключением: %s</span><div class='frame'>" % (len(reconnect_stat))
            for i in range(len(reconnect_stat)):
                output += "<div><span class='show'>Заявка на подключение к потоку:%s, подключил к:%s</span>" % (aor.streams[reconnect_stat[i]['route']], aor.streams[reconnect_stat[i]['stream']])
                output += "<div class='frame'>"
                if len(reconnect_log[i]) == 2:
                    for l in reconnect_log[i][1]:
                        output += "Понизил с потока:%s, на поток:%s, пропускную способность с: %s, до: %s<br />" % (aor.streams[l['from']], aor.streams[l['to']], l['value'], l['decreased'])


                for l in aor.flatten(reconnect_log[i][0]):
                        output += "Переподключил с потока:%s, на поток:%s, пропускную способность : %s<br />" % (aor.streams[l['from_stream']], aor.streams[l['to_stream']], l['value'])


                output += "</div></div>"
            output += "</div></div>"
            stat.reconnect = output
        else: stat.reconnect = "&nbsp;"

        if len(query_stat):
            output = "<div><span class='show'>Длина очереди: %s</span><div class='frame'>" % (len(query_stat))
            for s in query_stat:
                output += "Поток:%s, время появления:%s, алгоритм подключения:%s<br />" % (aor.streams[s['route']], s['step'], s['algorithm'])
            output += "</div></div>"
            stat.query = output
        else: stat.query = "&nbsp;"

        stat.connect_count = connect_count
        stat.query_count = query_count
        stat.disconnect_count = disconnect_count
        stat.connect_success_count = connect_success_count
        stat.connect_failure_count = connect_failure_count
        stat.reconnect_success_count = reconnect_success_count
        stat.reconnect_failure_count = reconnect_failure_count
        stat.save()

        for point_id in points:
            p = points[point_id]
            node_loading_stat = NodeLoadingStat()
            node_loading_stat.step = step
            node_loading_stat.loading = loading
            node_loading_stat.node = p


            if p.loading:
                func = aod.get_function(p.loading.ob_algorithm)
                node_loading_stat.output_bandwidth = (p.output_bandwidth * p.loading.max_output_bandwidth / 100) + p.overload - func((p.loading.min_output_bandwidth / 100.0) * p.output_bandwidth, (p.loading.max_output_bandwidth / 100.0) * p.output_bandwidth)
                func = aod.get_function(p.loading.ib_algorithm)
                node_loading_stat.input_bandwidth = p.overload2 - func((p.loading.min_input_bandwidth / 100.0) * p.input_bandwidth, (p.loading.max_input_bandwidth / 100.0) * p.input_bandwidth)
                func = aod.get_function(p.loading.cpu_algorithm)
                node_loading_stat.cpu = func((p.loading.min_cpu / 100.0) * p.cpu, (p.loading.max_cpu / 100.0) * p.cpu)
                func = aod.get_function(p.loading.memory_algorithm)
                node_loading_stat.memory = func((p.loading.min_memory / 100.0) * p.memory, (p.loading.max_memory / 100.0) * p.memory)
            else:
                node_loading_stat.output_bandwidth = p.overload
                node_loading_stat.input_bandwidth = p.overload2
                node_loading_stat.cpu = p.cpu
                node_loading_stat.memory = p.memory

            node_loading_stat.users = points[point_id].user_count
            node_loading_stat.overload = points[point_id].overload

            if loading.mode in ['0', '2']:
                node_loading_stat.save()

        for stream_id in aor.streams:
            s = aor.streams[stream_id]
            route_loading_stat = RouteLoadingStat()
            route_loading_stat.step = step
            route_loading_stat.loading = loading
            route_loading_stat.route = aor.streams[stream_id]
            if s.loading:
                func = aod.get_function(s.loading.algorithm)
                min_bandwidth = s.bandwidth - s.loading.min_bandwidth
                if min_bandwidth < 0: min_bandwidth = 0
                max_bandwidth = s.bandwidth + s.loading.max_bandwidth
                route_loading_stat.bandwidth = func(min_bandwidth, max_bandwidth)
            else:
                route_loading_stat.bandwidth = s.bandwidth
            route_loading_stat.users = aor.streams[stream_id].user_count

            if loading.mode in ['0', '3']:
                route_loading_stat.save()

    elapsed = (time.time() - start_time)
    print "Прошло времени: %s" % elapsed

    return redirect('loms:user_stat', pk=pk)

def user_stat_delete(request, pk):
    loading = get_object_or_404(Loading, pk=pk)
    LoadingStat.objects.filter(loading=loading).delete()
    NodeLoadingStat.objects.filter(loading=loading).delete()
    RouteLoadingStat.objects.filter(loading=loading).delete()
    return redirect('loms:index')

def route_stat(request, pk):
    loading = get_object_or_404(Loading, pk=pk)
    network_map = loading.network_map

    if RouteLoadingStat.objects.filter(loading=loading).count() > 0:
        routes_stat = RouteLoadingStat.objects.filter(loading=loading)
        return render(request, 'loms/route_stat.html',
            {'loading': loading, 'routes_stat': routes_stat })

    for i in xrange(1, loading.steps + 1):
        ids = {}
        routes = Route.objects.filter(start_node__network_map=network_map).order_by('step')
        for idx, route in enumerate(routes):
            route_loading_stat = RouteLoadingStat()
            route_loading_stat.step = i
            route_loading_stat.loading = loading
            route_loading_stat.route = route

            route_loadings = RouteLoading.objects.filter(loading=loading, route=route)
            if len(route_loadings) > 0:
                    route_loading = route_loadings[0]

                    if route.start_node == route.end_node:
                        if route.parent:
                            bandwidth = route.bandwidth - (route.parent.bandwidth - ids[route.parent.pk].bandwidth)
                            if bandwidth < 0: bandwidth = 0
                        else:
                            bandwidth = route.bandwidth
                    else:
                        if route.parent:
                            bandwidth = ids[route.parent.pk].bandwidth
                        else:
                            bandwidth = route.bandwidth

                    min_bandwidth = bandwidth - route_loading.min_bandwidth
                    if min_bandwidth < 0: min_bandwidth = 0
                    max_bandwidth = bandwidth + route_loading.max_bandwidth
                    func = aod.get_function(route_loading.algorithm)
                    route_loading_stat.bandwidth = func(min_bandwidth, max_bandwidth)
            else:
                if route.start_node == route.end_node:
                    if route.parent:
                        route_loading_stat.bandwidth = route.bandwidth - (route.parent.bandwidth - ids[route.parent.pk].bandwidth)
                        if route_loading_stat.bandwidth < 0: route_loading_stat.bandwidth = 0
                    else:
                        route_loading_stat.bandwidth = route.bandwidth
                else:
                    if route.parent:
                        route_loading_stat.bandwidth = ids[route.parent.pk].bandwidth
                    else:
                        route_loading_stat.bandwidth = route.bandwidth

            route.bandwidth = route_loading_stat.bandwidth
            ids[route.pk] = route
            route_loading_stat.save()

    return redirect('loms:route_stat', pk=pk)

class LoadingAdd(edit.CreateView):
    model = Loading
    def get_success_url(self):
        return  reverse_lazy('loms:detail', kwargs={'pk': self.object.id })

class LoadingAddForm(forms.ModelForm):
    class Meta:
        model = Loading
        exclude = ('network_map', )

class LoadingUpdate(edit.UpdateView):
    model = Loading
    form_class = LoadingAddForm
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return  reverse_lazy('loms:index')

class LoadingDelete(edit.DeleteView):
    model = Loading
    def get_success_url(self):
        return  reverse_lazy('loms:index')


def user_loading_addformset(request, pk1, pk2):
    loading = get_object_or_404(Loading, pk=pk1)
    route = get_object_or_404(Route, pk=pk2)
    UserLoadingFormSet = modelformset_factory(UserLoading, widgets={'algorithm': forms.Select(choices=aoc.get_names()), 'route': forms.HiddenInput, 'loading': forms.HiddenInput }, can_delete=True)

    if request.method == 'POST':
        formset = UserLoadingFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instance = formset.save()
            formset = UserLoadingFormSet(initial=[{'route':route, 'loading':loading}], queryset=UserLoading.objects.filter(loading=loading, route=route))
    else:
        formset = UserLoadingFormSet(initial=[{'route':route, 'loading':loading}], queryset=UserLoading.objects.filter(loading=loading, route=route))

    return render_to_response('loms/user_loading_add_formset.html', {'formset':formset, 'pk1':pk1, 'pk2':pk2 });

class UserLoadingAddForm(forms.Form):
    user_loading_route = forms.ModelChoiceField(label=_('Main Route'), queryset=Route.objects.all(), widget=forms.Select(attrs={'class': 'selector'}))

def user_loading_add(request, pk, pk1, pk2):
    loading = get_object_or_404(Loading, pk=pk)
    start_node = get_object_or_404(Node, pk=pk1)
    end_node = get_object_or_404(Node, pk=pk2)

    form = UserLoadingAddForm()
    form.fields['user_loading_route'].queryset = Route.objects.filter(start_node=start_node, end_node=end_node)
    return render_to_response('loms/user_loading_add.html', {'form':form, 'pk':pk, 'pk1':pk1, 'pk2':pk2 });

class RouteLoadingUpdateListForm(forms.Form):
    loading_route = forms.ModelChoiceField(label=_('Main Route'), queryset=RouteLoading.objects.all(), widget=forms.Select(attrs={'class': 'selector'}))

def route_loading_update_list(request, pk, pk1, pk2):
    loading = get_object_or_404(Loading, pk=pk)
    start_node = get_object_or_404(Node, pk=pk1)
    end_node = get_object_or_404(Node, pk=pk2)
    form = RouteLoadingUpdateListForm()
    form.fields['loading_route'].queryset = RouteLoading.objects.filter(Q(Q(route__start_node=start_node, route__end_node=end_node) | Q(route__start_node=end_node, route__end_node=start_node), loading=loading))
    return render_to_response('loms/route_loading_update_list.html', {'form':form, 'pk':pk, 'pk1':pk1, 'pk2':pk2 });


class RouteLoadingUpdateForm(ModelForm):
    class Meta:
        model = RouteLoading
        exclude = ('loading','route')
        widgets = {
            'algorithm': forms.Select(choices=aod.get_names())
        }

def route_loading_update(request, pk, route_loading_pk):
    loading = get_object_or_404(Loading, pk=pk)
    route_loading = get_object_or_404(RouteLoading, pk=route_loading_pk)

    if request.method == 'POST':
        form = RouteLoadingUpdateForm(request.POST, instance=route_loading)
        if form.is_valid():
            instance = form.save(commit=False)
            #instance.loading = loading
            instance.save()
            return HttpResponse(serializers.serialize('json', [instance]), content_type='application/json')
    else:
        form = RouteLoadingUpdateForm(instance=route_loading)

    return render_to_response('loms/route_loading_update.html', {'form':form, 'pk':pk, 'route_loading': route_loading });

class RouteLoadingAddForm(ModelForm):
    class Meta:
        model = RouteLoading
        exclude = ('loading',)
        widgets = {
            'algorithm': forms.Select(choices=aod.get_names())
        }

def route_loading_add(request, pk, pk1, pk2):
    loading = get_object_or_404(Loading, pk=pk)
    start_node = get_object_or_404(Node, pk=pk1)
    end_node = get_object_or_404(Node, pk=pk2)

    if request.method == 'POST':
        form = RouteLoadingAddForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.loading = loading
            instance.save()
            return HttpResponse(serializers.serialize('json', [instance]), content_type='application/json')
    else:
        form = RouteLoadingAddForm()

    form.fields['route'].queryset = Route.objects.filter(Q(Q(start_node=start_node, end_node=end_node) | Q(start_node=end_node, end_node=start_node)) & ~Q(routeloading__loading=loading))
    return render_to_response('loms/route_loading_add.html', {'form':form, 'pk':pk, 'pk1':pk1, 'pk2':pk2 });


class RouteLoadingDeleteForm(forms.Form):
    route_loading = forms.ModelChoiceField(queryset=RouteLoading.objects.all(), required=False)

def user_loading_delete(request, pk, pk1, pk2):
    pass

def route_loading_delete(request, pk, pk1, pk2):
    loading = get_object_or_404(Loading, pk=pk)
    node_from = get_object_or_404(Node, pk=pk1)
    node_to = get_object_or_404(Node, pk=pk2)
    if request.method == 'POST':
        form = RouteLoadingDeleteForm(request.POST)
        if(form.is_valid()):
            data = form.cleaned_data
            if data['route_loading']:
                route_loading = data['route_loading']
                pk = route_loading.pk
                route_loading.delete()
                return HttpResponse(pk, content_type='application/json')
    form = RouteLoadingDeleteForm()
    form.fields['route_loading'].queryset = RouteLoading.objects.filter(Q(Q(route__start_node=node_from, route__end_node=node_to) | Q(route__start_node=node_to, route__end_node=node_from)) & Q(loading=loading))
    return render_to_response('loms/route_loading_delete.html',
        {'form':form, 'pk':pk, 'pk1':pk1, 'pk2':pk2 } );


class LoadingCopyForm(forms.Form):
    name = forms.CharField(max_length=200, label=_('Name'))

def loading_copy(request, pk):
    loading = get_object_or_404(Loading, pk=pk)
    loading_pk = loading.pk
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = LoadingCopyForm(request.POST)
            if form.is_valid():
                loading.name = form.cleaned_data['name']
                loading.pk = None
                loading.save()
                for route_loading in RouteLoading.objects.filter(loading=loading_pk):
                    route_loading.pk = None
                    route_loading.loading = loading
                    route_loading.save()

                for node_loading in NodeLoading.objects.filter(loading=loading_pk):
                    node_loading.pk = None
                    node_loading.loading = loading
                    node_loading.save()

                for user_loading in UserLoading.objects.filter(loading=loading_pk):
                    user_loading.pk = None
                    user_loading.loading = loading
                    user_loading.save()

                return redirect('loms:index')
        else:
            form = LoadingCopyForm()
        return render_to_response('loms/loading_copy.html', {'form':form, 'loading_pk':loading.pk})
    else:
        return HttpResponse("<h1>You Are Not Authorized to View This Page</h1>")

class NodeLoadingUpdateForm(ModelForm):
    class Meta:
        model = NodeLoading
        exclude = ('loading', 'node')
        widgets = {
            'ib_algorithm': forms.Select(choices=aod.get_names()),
            'ob_algorithm': forms.Select(choices=aod.get_names()),
            'cpu_algorithm': forms.Select(choices=aod.get_names()),
            'memory_algorithm': forms.Select(choices=aod.get_names())
        }

def node_loading_update(request, loading_pk, node_pk):
    loading = get_object_or_404(Loading, pk=loading_pk)
    node = get_object_or_404(Node, pk=node_pk)
    node_loading = NodeLoading.objects.get(loading=loading, node=node)

    if request.method == 'POST':
        form = NodeLoadingAddForm(request.POST, instance=node_loading)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponse(serializers.serialize('json', [instance]), content_type='application/json')
    else:
        form = NodeLoadingAddForm(instance=node_loading)

    return render_to_response('loms/node_loading_update.html', {'form':form, 'loading_pk':loading_pk, 'node_pk':node_pk });

class NodeLoadingAddForm(ModelForm):
    class Meta:
        model = NodeLoading
        exclude = ('loading', 'node')
        widgets = {
            'ib_algorithm': forms.Select(choices=aod.get_names()),
            'ob_algorithm': forms.Select(choices=aod.get_names()),
            'cpu_algorithm': forms.Select(choices=aod.get_names()),
            'memory_algorithm': forms.Select(choices=aod.get_names())
        }

def node_loading_add(request, loading_pk, node_pk):
    loading = get_object_or_404(Loading, pk=loading_pk)
    node = get_object_or_404(Node, pk=node_pk)
    if NodeLoading.objects.filter(loading=loading, node=node).count() > 0:
        raise Http404

    if request.method == 'POST':
        form = NodeLoadingAddForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.loading = loading
            instance.node = node
            instance.save()
            return HttpResponse(serializers.serialize('json', [instance]), content_type='application/json')
    else:
        form = NodeLoadingAddForm(initial={
            'input_bandwidth':node.input_bandwidth,
            'output_bandwidth':node.output_bandwidth,
            'cpu':node.cpu,
            'memory':node.memory
        })

    return render_to_response('loms/node_loading_add.html', {'form':form, 'loading_pk':loading_pk, 'node_pk':node_pk });

def node_loading_delete(request, loading_pk, node_pk):
    loading = get_object_or_404(Loading, pk=loading_pk)
    node = get_object_or_404(Node, pk=node_pk)
    node_loading = get_object_or_404(NodeLoading, loading=loading, node=node)
    if request.method == 'POST':
        pk = node_loading.pk
        node_loading.delete()
        return HttpResponse(pk, content_type='application/json')
    return render_to_response('loms/node_loading_delete.html',
        {'loading_pk':loading_pk, 'node_pk':node_pk} );
