from main.models import ContactMessage, UpdateMessage
from django.contrib import admin   
class ContactMessageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['subject']}),
        (None, {'fields': ['email']}),
        (None, {'fields': ['content']}),
    ]
    list_display = ('subject', 'time', 'name', 'user', 'id')
    list_filter = ['name']
    search_fields = ['name', 'subject', 'email']
    date_hierarchy = 'time'
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

class UpdateMessageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['level']}),
        (None, {'fields': ['title']}),
        (None, {'fields': ['message']}),
        (None, {'fields': ['priority']}),
        (None, {'fields': ['cookie_max_age']}),
        (None, {'fields': ['expire_time']}),
        (None, {'fields': ['users_log']}),
        (None, {'fields': ['expired']}),
    ]
    list_display = ('title', 'level', 'priority', 'cookie_max_age', 'time', 'expired')
    list_filter = ['level']
    search_fields = ['message', 'users_log', 'level']
    date_hierarchy = 'time'
      
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(UpdateMessage, UpdateMessageAdmin)
