from django.conf.urls import patterns, url, include
from soms import views

node_patterns = patterns('',
    url(r'^/$', views.NodeIndex.as_view(), name='index'),
    url(r'^/add/$', views.NodeAdd.as_view(), name='add'),
    url(r'^/(?P<pk>\d+)/delete/$', views.NodeDelete.as_view(), name='delete'),
    url(r'^/move/$', views.node_move, name='move'),
    url(r'^/move/(?P<pk>\d+)/(?P<x>\d+)/(?P<y>\d+)/$', views.node_move),
    url(r'^/(?P<pk>\d+)/delete/json/$', views.node_delete_json, name='delete_json'),
    url(r'^/(?P<pk>\d+)/$', views.NodeUpdate.as_view(), name='update'),
    url(r'^/(?P<pk>\d+)/json/$', views.node_json, name='json'),
)

track_patterns = patterns('',
    url(r'^/$', views.TrackIndex.as_view(), name='index'),
    url(r'^/add/(?P<pk>\d+)/$', views.TrackAdd.as_view(), name='add'),
    url(r'^/(?P<pk>\d+)/delete/$', views.TrackDelete.as_view(), name='delete'),
    url(r'^/(?P<pk>\d+)/delete/json/$', views.track_delete_json, name='delete_json'),
    url(r'^/(?P<pk>\d+)/$', views.TrackUpdate.as_view(), name='update'),
    url(r'^/(?P<pk>\d+)/json/$', views.track_json, name='json'),
)
link_patterns = patterns('',
    url(r'^/$', views.TrackIndex.as_view(), name='index'),
    url(r'^/add/(?P<pk>\d+)/$', views.LinkAdd.as_view(), name='add'),
    url(r'^/(?P<pk>\d+)/delete/$', views.LinkDelete.as_view(), name='delete'),
    url(r'^/(?P<pk>\d+)/delete/json/$', views.link_delete_json, name='delete_json'),
    url(r'^/(?P<pk>\d+)/json/$', views.link_json, name='json'),
)

route_patterns = patterns('',
    url(r'^/add/$', views.route_add, name='add'),
    url(r'^/add/(?P<pk1>\d+)/(?P<pk2>\d+)/$', views.route_add, name='add_nodes'),
    url(r'^/delete/$', views.route_delete, name='delete'),
    url(r'^/delete/(?P<pk1>\d+)/(?P<pk2>\d+)/$', views.route_delete, name='delete_nodes'),
    url(r'^/(?P<pk>\d+)/delete/json/$', views.route_delete_json, name='delete_json'),
    url(r'^/detail/$', views.route_detail, name='detail'),
    url(r'^/detail/(?P<pk>\d+)/$', views.route_detail, name='detail_routes'),
)

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^documents/$', views.documents, name='documents'),
    url(r'^model/$', views.modelka, name='modelka'),
    url(r'^main/$', views.main, name='main'),
    url(r'^(?P<pk>\d+)/$', views.detail, name='detail'),

    url(r'^add/$', views.AddNetworkMap, name='add'),

    url(r'^(?P<pk>\d+)/update/$', views.NetworkMapUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/update1/$', views.NetworkMapUpdateForm.as_view(), name='update_for_model'),
    url(r'^(?P<pk>\d+)/delete/$', views.NetworkMapDelete.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/copy/$', views.networkmap_copy, name='copy'),
    url(r'^(?P<pk>\d+)/node/json/$', views.networkmap_node_json, name='networkmap_node_json'),
    url(r'^(?P<pk>\d+)/track/json/$', views.networkmap_track_json, name='networkmap_track_json'),
    url(r'^(?P<pk>\d+)/route/json/$', views.networkmap_route_json, name='networkmap_route_json'),
    url(r'^(?P<pk>\d+)/link/json/$', views.networkmap_link_json, name='networkmap_link_json'),
    url(r'^node', include(node_patterns, 'node')),
    url(r'^track', include(track_patterns, 'track')),
    url(r'^route', include(route_patterns, 'route')),
    url(r'^link', include(link_patterns, 'link')),
)
