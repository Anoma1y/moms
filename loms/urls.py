from django.conf.urls import patterns, url, include
from loms import views

route_loading_patterns = patterns('',
    url(r'^/add(?:/(?P<pk>\d+)/(?P<pk1>\d+)/(?P<pk2>\d+))?/$', views.route_loading_add, name='add'),
    url(r'^/delete(?:/(?P<pk>\d+)/(?P<pk1>\d+)/(?P<pk2>\d+))?/$', views.route_loading_delete, name='delete'),
    url(r'^/update_list(?:/(?P<pk>\d+)/(?P<pk1>\d+)/(?P<pk2>\d+))?/$', views.route_loading_update_list, name='update_list'),
    url(r'^/update(?:/(?P<pk>\d+)/(?P<route_loading_pk>\d+))?/$', views.route_loading_update, name='update'),
)

node_loading_patterns = patterns('',
    url(r'^/add(?:/(?P<loading_pk>\d+)/(?P<node_pk>\d+))?/$', views.node_loading_add, name='add'),
    url(r'^/delete(?:/(?P<loading_pk>\d+)/(?P<node_pk>\d+))?/$', views.node_loading_delete, name='delete'),
    url(r'^/update(?:/(?P<loading_pk>\d+)/(?P<node_pk>\d+))?/$', views.node_loading_update, name='update'),
)

user_loading_patterns = patterns('',
    url(r'^/add(?:/(?P<pk>\d+)/(?P<pk1>\d+)/(?P<pk2>\d+))?/$', views.user_loading_add, name='add'),
    url(r'^/addformset(?:/(?P<pk1>\d+)/(?P<pk2>\d+))?/$', views.user_loading_addformset, name='addformset'),
    url(r'^/delete(?:/(?P<pk>\d+)/(?P<pk1>\d+)/(?P<pk2>\d+))?/$', views.user_loading_delete, name='delete'),

)

chart_patterns = patterns('',
    url(r'^/loading/$', views.loading_chart, name='loading'),
    url(r'^/node/$', views.node_list_chart, name='node_list'),
    url(r'^/node(?:/(?P<node_pk>\d+))?/$', views.node_chart, name='node'),
    url(r'^/route/$', views.route_list_chart, name='route_list'),
    url(r'^/route(?:/(?P<route_pk>\d+))?/$', views.route_chart, name='route'),
)

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>\d+)/user-stat/$', views.user_stat, name='user_stat'),
    url(r'^(?P<pk>\d+)/user-stat/delete/$', views.user_stat_delete, name='user_stat_delete'),
    url(r'^add/$', views.LoadingAdd.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/update/$', views.LoadingUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.LoadingDelete.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/copy/$', views.loading_copy, name='copy'),
    url(r'^route', include(route_loading_patterns, 'route')),
    url(r'^node', include(node_loading_patterns, 'node')),
    url(r'^user', include(user_loading_patterns, 'user')),
    url(r'^(?P<pk>\d+)/chart', include(chart_patterns, 'chart')),
)
