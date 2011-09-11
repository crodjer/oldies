from django_cron.models import *
from django.contrib import admin
            
class JobAdmin(admin.ModelAdmin):
    list_display = ('name','run_frequency', 'last_run', 'instance','queued',)

class CronAdmin(admin.ModelAdmin):
    list_display = ('executing',)
    
admin.site.register(Job, JobAdmin)
admin.site.register(Cron, CronAdmin)