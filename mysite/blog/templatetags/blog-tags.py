from django import template
from django.core.urlresolvers import reverse
import urllib, hashlib
from blog.models import Post
register = template.Library()

@register.simple_tag
def get_index_page(post, user):    
    return  post.get_index_page(user)

@register.simple_tag
def get_subscribe_link(post, user):
    subs_str = '<a href="%s">%s</a>'
    if user and user in post.subscribers.all():
        return subs_str %(reverse('blog:unsubscribe', args=[post.slug]), 'Unsubscribe from post')
    else:
        return subs_str %(reverse('blog:subscribe', args=[post.slug]), 'Subscribe to post')        
        
