from django.contrib import messages 
from main.models import  UpdateMessage
from django.http import HttpResponse
import datetime
import re

class MyMiddleware:
    def __init__(self):
        #print 'Initialized my Middleware'
        pass
    
    def process_request(self, request):        
        user_id = False
        if request.user.is_active:                
            user_id = str(request.user.id)                            
        self.process_update_messages(request, user_id)
        self.process_referer(request)
    
    def process_referer(self, request):
        referer = request.META.get('HTTP_REFERER', False)                    
        if referer:
            pattern = re.compile(r'http://(?P<word>[\w,.]*)')
            try:
                r = pattern.search(referer).group('word')
                if 'www.google.com/url?q=http%3A%2F%2Fwww.rohanjain.in%2Fcontact%2F&sa=D&sntz=1&usg=AFQjCNEh8GZZ0R_6dvMillfElKMavXCHwA' in referer:
                    messages.success(request, 'Thanks for checking out my resume.')
                elif 'www.google' in r:
                    messages.success(request, 'Thanks for googling me on the web.')
                elif 'facebook' in r:
                    messages.success(request, 'Thanks for checking out my facebook profile.')
                elif 'stackoverflow' in r:
                    messages.success(request, 'Thanks for visiting my StackOverflow profile.')
                elif 'academia.edu' in r:
                    messages.success(request, 'Thanks for checking out my academia profile.')
                elif 'localhost' in r:
                    #messages.success(request, 'Just a test: ' + referer)
                    pass
            except:
                pass 
                                                            
    def process_response(self, request, response):
        self.process_update_messages_response(request, response)
        return response
    
    def process_update_messages(self, request, user_id=False):
        update_messages = UpdateMessage.objects.exclude(expired=True)         
        render_message = False 
        request.session['update_messages'] = []
        for message in update_messages:                        
            if message.expire_time < datetime.datetime.now():
                message.expired = True
                message.save()
            else:                
                if request.COOKIES.get(message.cookie(), True) == True:
                    render_message = True
                    
                '''                           
                if user_id:
                    users_log = message.users_log.split(';')
                    if user_id in users_log:
                        #render_message = False
                        pass
                    else:
                        message.users_log+=user_id+';'
                        message.save()
                '''
                if render_message:
                    request.session['update_messages'].append({'cookie': message.cookie(), 'cookie_max_age': message.cookie_max_age})
                    messages.add_message(request, message.level, message)
                    break
                    
    def process_update_messages_response(self, request, response):
        try:
            update_messages = request.session['update_messages']
        except:
            update_messages = False
        if update_messages:            
            for message in update_messages:
                response.set_cookie(message['cookie'], value=False, max_age=message['cookie_max_age'], expires=None, path='/', domain=None, secure=None)
        return response
