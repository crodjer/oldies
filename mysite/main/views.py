from django.shortcuts import render_to_response, redirect
from main.models import ContactMessageForm, RecaptchaForm
from blog.models import Post
from django.http import HttpResponse
from django.core.urlresolvers import reverse 
from django.core.cache import cache
from django.contrib import messages
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from urllib2 import urlopen
from markdown import markdown

def home(request):
    home_post = Post.objects.get(title="Home")
    updates = Post.objects.get_updates(request.user)
    return render_to_response('main/home.html', {'home':True, 'home_post':home_post, 'updates':updates}, context_instance=RequestContext(request))

def contact(request):
    recaptcha_form = False
    human_verified = request.session.get('human_verified', False)
    if not human_verified:
        recaptcha_form = RecaptchaForm()        
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)            
        if form.is_valid():   
            new_contact_message = form.save(commit=False)
            if request.user.is_active:
                new_contact_message.user = request.user
            else:                
                new_contact_message.user = User.objects.get_or_create(username = 'anonymous', email = 'noemail@rohanjain.in' )[0]
            new_contact_message.save()
            if new_contact_message.send():
                messages.success(request, _('Your message was sent to the managers, we will respond soon.'))
            else:
                messages.error(request, _('An error occured in sending the mail.'))
            return redirect('main:home')
        else:
            messages.error(request, _('Some errors were found in you contact form.'))
    else:
        form = ContactMessageForm()
    return render_to_response('main/contact.html', {'form': form, 'contact':True, 'recaptcha_form':recaptcha_form, 'human_verified': human_verified}, context_instance=RequestContext(request))


def message(request, type, message):     
    if type == 'success': 
        messages.success(request, message)
    elif type == "info":
        messages.info(request, message)
    else:
        messages.error(request, message)    
    return redirect('main:home')


def recaptcha(request):    
    if request.session.get('human_verified', False):
        return render_to_response('main/recaptcha.html', {'human_verified': True }, context_instance=RequestContext(request))
    else:        
        if request.method=="POST":
            form = RecaptchaForm(request.POST)
            next = request.POST.get('next', False)                
            if form.is_valid():               
                request.session['human_verified']=True
                messages.success(request, _('You have been successfully verified as a human.'))
                return redirect(next)
            else: 
                messages.error(request, _('Some error occured in your recaptcha submission.'))
        else:
            form = RecaptchaForm()        
            next = reverse('main:recaptcha')
        return render_to_response('main/recaptcha.html', {'form': form, 'next':next }, context_instance=RequestContext(request))            

def mdtohtml(request):
    url = request.GET.get('u')
    print url
    if url:
        key = 'markdown_url:%s' %(url)
        html = cache.get(key)
        if not html:
            text = urlopen(url).read()
            html = markdown(text)
            cache.set(key, html, 600)
        return HttpResponse(html)
    else:
        return HttpResponse('Please provide a url (GET variable: u) to convert to markdown.')
