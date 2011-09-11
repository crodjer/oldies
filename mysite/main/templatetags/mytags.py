import urllib
import hashlib
from django import template
from django.contrib.sites.models import Site
import settings

ABSOLUTE_MEDIA_URL = settings.MEDIA_URL
if not ABSOLUTE_MEDIA_URL.startswith('http://'):
    ABSOLUTE_MEDIA_URL = 'http://%s%s' %(Site.objects.get_current().domain, ABSOLUTE_MEDIA_URL)
register = template.Library()

@register.simple_tag
def gravatar(email):        
    size = 50
    default = "%simg/avatar-default.jpg" %(ABSOLUTE_MEDIA_URL)
    url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"    
    url += urllib.urlencode({'d':default, 's':str(size)})
    return '<a href="http://gravatar.com/emails/" target="_blank"><img src="%s"/></a>' %(url.replace('&', '&amp;')) 
    
