from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to
from blog.feeds import BlogFeed

urlpatterns = patterns('blog.views',
    url(r'^$', 'index', name = 'index'),
    url(r'^index/(?P<page_no>\d+)/$', 'index', name = 'index-page'),
    url(r'^feed/$', BlogFeed()),    
    url(r'^new/$', 'new', name = 'blog-new'),
    url(r'^(?P<post_slug>[-\w]+)/$', 'post', name = 'post'),    
    url(r'^(?P<post_slug>[-\w]+)/edit/$', 'edit', name = 'edit'),
    url(r'^(?P<post_slug>[-\w]+)/publish/$', 'publish', name = 'publish'),
    url(r'^(?P<post_slug>[-\w]+)/delete/$', 'delete', name = 'delete'),
    url(r'^(?P<post_slug>[-\w]+)/subscribe/$', 'subscribe', name = 'subscribe'),
    url(r'^(?P<post_slug>[-\w]+)/unsubscribe/$', 'unsubscribe', name = 'unsubscribe'),
    url(r'^(?P<post_slug>[-\w]+)/unsubscribe/(?P<user_id>\d+)/(?P<email>[-_.@\w]+)/$', 'unsubscribe', name = 'unsubscribe-by-mail'),
    (r'^post/(?P<post_slug>[-\w]+)/$', redirect_to, {'url': '/blog/%(post_slug)/'}),
    url(r'^(?P<post_slug>[-\w]+)/comment/$', redirect_to, {'url': '/blog/%(post_slug)s/#comment'}, name = 'comment-redirect'),
)
