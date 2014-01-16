from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.utils.encoding import force_unicode
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^', include('proj.tasks.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=force_unicode(settings.MEDIA_ROOT))
