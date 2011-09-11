from django.contrib.sitemaps import Sitemap, FlatPageSitemap
##import models from your apps here.
#like from main.models import YourModel
from blog.models import Post
import datetime

class AbstractSitemapClass():
    changefreq = 'daily'
    url = None
    def get_absolute_url(self):
        return self.url
    
class StaticSitemap(Sitemap):
    pages = {
             'home':'/', #Add more static pages here like this 'example':'url_of_example',
             'contact':'/contact/',
             'blog':'/blog/',
             }
    main_sitemaps = []
    for page in pages.keys():
        sitemap_class = AbstractSitemapClass()
        sitemap_class.url = pages[page]        
        main_sitemaps.append(sitemap_class)
    
    def items(self):
        return self.main_sitemaps    
    lastmod = datetime.datetime(2010, 8, 31)   #Enter the year,month, date you want in yout static page sitemap.
    priority = 1
    changefreq = "yearly"                        #Enter The frequency with which static pages changes.    
    
class MyFlatPageSitemap(FlatPageSitemap):
    changefreq = "weekly"
    priority = 0.6    
        
class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    #"Model" is your model name.
    def items(self):
        return Post.objects.filter(publish=True)
    def lastmod(self, obj):
        return obj.updated_on
    
    
sitemaps = {
            'main':StaticSitemap,
            'flatpages':MyFlatPageSitemap,
            'model':PostSitemap,
            }

    
