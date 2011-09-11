from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template':'movie/home.html'}),
    (r'^list/$', 'movie.views.list_movie'),
    (r'^add/$', direct_to_template, {'template':'movie/add.html'}),
    (r'^saving/$','movie.views.saving'),
    (r'^save/$', 'movie.views.save'),
    (r'^save_status/$', 'movie.views.save_status'),
    (r'^search/$', 'movie.views.search'),                           
    #(r'^page/$', 'main.views.page'),
    (r'^(?P<movie_id>\d+)/$', 'movie.views.movie_details'),
)
