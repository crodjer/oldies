from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
import settings
from sitemaps import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('main.urls', namespace="main")),
    (r'^blog/', include('blog.urls', namespace="blog")),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^openid/', include('django_openid_auth.urls')),
    (r'^accounts/', include('django_openid_auth.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),    
    url(r'^ie/$', direct_to_template, {'template':'includes/ie-error.html'}, name='ie-error'),
    url(r'^old-browser/$', direct_to_template, {'template':'includes/old-browser.html'}, name='old-browser'),
    url(r'^robots.txt$', direct_to_template, {'template':'main/robots.txt', 'mimetype': 'text/plain'}, name='robots'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='sitemap'),
)

if settings.DEBUG:
    urlpatterns+=url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),                       
