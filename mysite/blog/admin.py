from blog.models import Post
from django.contrib import admin
    
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        (None, {'fields': ['slug']}),
        (None, {'fields': ['user']}),
        (None, {'fields': ['description']}),
        (None, {'fields': ['content']}),
        (None, {'fields': ['subscribers']}),
        (None, {'fields': ['comments_allowed']}),
        (None, {'fields': ['is_update']}),
        (None, {'fields': ['publish']}),        
    ]
    list_display = ('title', 'user', 'description', 'added_on', 'updated_on', 'publish', 'comments_allowed', 'is_update')
    list_filter = ['added_on', 'updated_on', 'is_update', 'publish']
    filter_horizontal = ('subscribers', )
    search_fields = ['title', 'description']
    date_hierarchy = 'added_on'    
admin.site.register(Post, PostAdmin)
