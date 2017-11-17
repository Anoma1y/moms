from django.conf.urls import patterns, include, url
import soms.views

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', soms.views.main),
    url(r'^soms/', include('soms.urls', namespace="soms")),
    url(r'^loms/', include('loms.urls', namespace="loms")),
    url(r'^admin/', include(admin.site.urls), name='admin'),
)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)