from movie.models import *
from django.contrib import admin
class DownloadInfoInline(admin.TabularInline):
    model = DownloadInfo
    extra = 0
    
class MovieAdmin(admin.ModelAdmin):
    inlines = [DownloadInfoInline]
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['rating']}),
        (None,               {'fields': ['year']}),
        (None,               {'fields': ['image']}),        
        (None,               {'fields': ['plot']}),
        (None,               {'fields': ['release_date']}),
        (None,               {'fields': ['genre']}),
        (None,               {'fields': ['director']}),
        (None,               {'fields': ['writers']}),
        (None,               {'fields': ['stars']}),        
        (None,               {'fields': ['imdb_url']}),
        
    ]
    list_display = ('name','rating', 'time','id',)
    list_filter = ['year', 'firstchar']
    search_fields = ['name','rating', 'plot','cast']
    date_hierarchy = 'time'
    
admin.site.register(Movie,MovieAdmin)
