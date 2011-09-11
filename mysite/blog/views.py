from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template import RequestContext
from blog.models import Post, PostForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from settings import DEFAULT_FROM_EMAIL, DEFAULT_SEND_EMAIL, SITE_ID
from django.contrib.sites.models import Site
from main.models import RecaptchaForm
from django.utils.translation import ugettext_lazy as _
import settings
DJANGO_COMMENTS = True

def index(request, page_no=1):
    paginator = Post.objects.get_paginated_posts(request.user)
    page = paginator.page(page_no)
    posts = page.object_list
    return render_to_response('blog/blog_index.html', {'posts':posts, 'page':page, 'blog':True, 'django_comments':DJANGO_COMMENTS}, context_instance=RequestContext(request))

def new(request):
    if not request.user.is_staff:
        messages.error(request, _('You dont have the permissions to create new posts.'))
        return redirect(index)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid(): 
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            post.subscribers.add(request.user)
            messages.success(request, 'Your post "%s" was published' % (post.title))
            return redirect(post)
        messages.error(request, _('Some errors were found in your post.'))
    else:
        form = PostForm()
    return render_to_response('blog/post_new.html', {'form': form, 'blog':True, 'django_comments':DJANGO_COMMENTS}, context_instance=RequestContext(request))

def edit(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    redirect_url = request.GET.get('next', post)
    if not request.user.has_perm('blog.change_post'):
        messages.error(request, _('You dont have the permissions to edit this post.'))
        return redirect(post)
    if request.method == 'POST':
        if request.POST['submit'] == "Save":
            redirect_url = request.META['PATH_INFO']
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.subscribers.add(request.user)
            messages.success(request, 'Your post "%s" was updated.' % (post.title))
            return redirect(redirect_url)
        messages.error(request, _('Some errors were found in your post.'))
    else:
        form = PostForm(instance=post)
    return render_to_response('blog/post_edit.html', {'form': form, 'post':post, 'blog':True, 'django_comments':DJANGO_COMMENTS}, context_instance=RequestContext(request))

def post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)    
    recaptcha_form = False
    human_verified = False
    comment_id = request.GET.get('c', None)    
    if request.session.get('human_verified', False):
        human_verified = True                    
    else:
        recaptcha_form = RecaptchaForm()
                
    if not post.publish and not request.user.has_perm('blog.change_post') and not request.GET.get('key', '') == post.key():
        messages.error(request, _('You don\'t have the permissions to view that post.'))
        return redirect(post.get_index_page())    
     
    if comment_id:
        if request.GET.get('flag', None):
            messages.success(request, 'The comment  was flagged')
        elif request.GET.get('delete', None):
            messages.success(request, 'The comment  was deleted')    
        elif request.GET.get('approve', None):
            messages.success(request, 'The comment was approved')    
        else:
            messages.success(request, 'Your comment on "%s" was published.' % (post.title))            
            comment = Comment.objects.get(pk=comment_id)
            if comment.user:
                post.subscribers.add(comment.user)                        
            comment_name = comment.user_name
            comment_email = comment.user_email
            title = post.title
            comment_content = comment.comment
            if comment.user:
                to_users = post.subscribers.exclude(pk=comment.user.pk)
            else:
                to_users = post.subscribers.all()
            formatted_subject = render_to_string('comments/comment_mail_subject.txt', {'title':title, 'name':comment_name }).replace('\n', '')                                            
            for user in to_users:
                link = 'http://%s%s' % (Site.objects.get_current().domain, post.get_absolute_url())
                unsubscribe_link = "%sunsubscribe/%s/%s" %(link, user.pk, user.email)
                text_content = render_to_string('comments/comment_mail_text.txt', {'title':title, 'comment':comment_content, 'email':comment_email, 'name':comment_name, 'link':link, 'comment_suffix':'#c%s' %(comment.id), 'unsubscribe_link':unsubscribe_link})
                html_content = render_to_string('comments/comment_mail_html.txt', {'title':title, 'comment':comment_content, 'email':comment_email, 'name':comment_name, 'link':link, 'comment_suffix':'#c%s' %(comment.id), 'unsubscribe_link':unsubscribe_link})                
                email = EmailMultiAlternatives(formatted_subject, text_content, 
                                     to=[user.email], 
                                    headers = {'Reply-To': comment_email})
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=settings.DEBUG)
        return redirect(post.get_absolute_url() + '#c' + comment_id)
    return render_to_response('blog/post.html', {'post':post, 'blog':False if post.is_update  else True, 'django_comments':DJANGO_COMMENTS, 'recaptcha_form':recaptcha_form, 'human_verified': human_verified}, context_instance=RequestContext(request))


def publish(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, user=request.user)
    redirect_url = request.GET.get('next', post)
    post.publish = True
    post.save()
    messages.success(request, _('Your post was successfully published.'))
    return redirect(redirect_url)

@login_required
def subscribe(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    post.subscribers.add(request.user)
    messages.success(request, 'You have successfully subscribed to the post: "%s".' % (post.title))
    return redirect(post)

def unsubscribe(request, post_slug, user_id=None, email=None):
    post = get_object_or_404(Post, slug=post_slug)          
    user = None
    if request.user.is_authenticated():
        user = request.user      
    
    elif user_id:
        user = get_object_or_404(User, id=user_id)
        if not user.email == email:
            user = None                                                             
        
    if user:                    
        post.subscribers.remove(user)
        messages.info(request, 'You successfully unsubscribed from the post: "%s".' % (post.title))    
    return redirect(post)

def delete(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, user=request.user)
    redirect_url = request.GET.get('next', post.get_index_page())
    post.publish = False
    post.save()
    messages.success(request, _('Your post was successfully unpublished.'))
    return redirect(redirect_url)
