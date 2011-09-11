from django.conf.urls.defaults import *
from django.contrib import admin
import settings, django_cron
django_cron.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('movie.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': False})
)
