from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
POSTS_PER_PAGE = 4

class PostManager(models.Manager):
    def get_paginated_posts(self, user=None):
        if user and user.has_perm('blog.change_post'):
            posts = super(PostManager, self).filter(is_update=False)
        else:
            posts = super(PostManager, self).filter(publish=True, is_update=False)
        return Paginator(posts, POSTS_PER_PAGE)

    def get_updates(self, user=None):
        if user and user.has_perm('blog.change_post'):
            updates = super(PostManager, self).filter(is_update=True)[:5]
        else:
            updates = super(PostManager, self).filter(is_update=True, publish=True)
        return updates

class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(unique=True)
    keywords = models.CharField(_('keywords'), max_length=200, blank=True)
    description = models.TextField(_('description'), max_length=300, blank=True)
    content = models.TextField(_('content'))        
    publish = models.BooleanField(_('publish on the web'), default=False)
    comments_allowed = models.BooleanField(_('allow comments on this post'), default=True)
    is_update = models.BooleanField(_('is an update'), default=False)
    added_on = models.DateTimeField(_('added on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)
    subscribers = models.ManyToManyField(User, related_name='subscribtions')
    objects = PostManager()    
    
    class Meta:
        get_latest_by = 'updated_on'
        ordering = ['-added_on']
    def __unicode__(self):
        return self.title[0].upper() + self.title[1:]
    def get_absolute_url(self):
        return '/blog/%s/' % (self.slug)
    def get_key_url(self):
        return self.get_absolute_url() + '?key=' + self.key()
    def get_page(self, user=None):
        return self._default_manager.filter(is_update = False, added_on__gt=self.added_on).count()/POSTS_PER_PAGE +1
    def key(self):
        key = ''
        slug = slugify(self.title).replace('-', '')
        for i in range(len(slug)):
            key += chr(ord(slug[i]) + 1)
        return key
    def get_subscribers(self):
        pass
    def get_index_page(self, user=None):
        page = self.get_page(user)
        if self.is_update:
            return reverse('main:home')
        elif page and page!=1:
            return reverse('blog:index-page', kwargs={'page_no':page})
        else:
            return reverse('blog:index')
    def save(self, *args, **kwargs):
        if self.id or self.slug:
            pass
        else:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'subscribers', 'slug')
    def clean_content(self):
        content = self.cleaned_data['content']
        if not strip_tags(content).replace('&nbsp;', '').replace(' ', ''):
            raise forms.ValidationError('Some text is required here.')
        return content.replace('<br>', '<br/>')
    def clean_title(self):
        title = self.cleaned_data['title']
        if not strip_tags(title).replace('&nbsp;', '').replace(' ', ''):
            raise forms.ValidationError('Some text is required here.')
        return title.replace('<br>', '')
