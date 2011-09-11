from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name = 'home'),
    url(r'^blank.html$', direct_to_template, {'template':'main/blank.html'}, name = 'blank'),
    url(r'^contact/$', 'main.views.contact', name = 'contact'),
    url(r'^contact/thanks/$', direct_to_template, {'template':'main/contact_thanks.html'}, name = 'contact-thanks'),
    url(r'^update/(?P<post_slug>[-\w]+)/$', 'blog.views.post', name = 'updates'),
    url(r'^message/(?P<type>\w+)/(?P<message>[\w\W]+)/$', 'main.views.message', name = 'test-message'),
    url(r'^recaptcha/$', 'main.views.recaptcha', name = 'recaptcha'),
    url(r'^markdown/$', 'main.views.mdtohtml', name = 'recaptcha'),
)
