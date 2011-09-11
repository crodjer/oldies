from django.db import models
from django.contrib.auth.models import User
from django import  forms
from django.utils.translation import ugettext_lazy as _
from settings import DEFAULT_FROM_EMAIL, DEFAULT_SEND_EMAIL
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from recaptcha_django import ReCaptchaField, ReCaptchaWidget
import settings

class ContactMessage(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField(_('Email'),)
    name = models.CharField(_('Name'), max_length=100)
    subject = models.CharField(_('Subject'), max_length=100)
    content = models.TextField(_('Message'))
    time = models.DateTimeField(_('Time'), auto_now_add=True)
    def __unicode__(self):
        return 'Message "%s" by "%s"' % (self.subject, self.user)
    def send(self):
        formatted_subject = render_to_string('main/contact_mail_subject.txt', {'subject':self.subject, 'name':self.name }).replace('\n', '')
        formatted_content = render_to_string('main/contact_mail.txt', {'subject':self.subject, 'content':self.content, 'email':self.email, 'name':self.name })
        mail = EmailMessage(formatted_subject, formatted_content,
                            DEFAULT_FROM_EMAIL, DEFAULT_SEND_EMAIL,
                            headers={'Reply-To': self.email})
        if mail.send(fail_silently=settings.DEBUG):
            return True
        else:
            return False

class UpdateMessage(models.Model):
    LEVELS = (
        (20, 'Info'),
        (25, 'Success'),
        (40, 'Failure'),
    )
    COOKIE_MAX_AGES = (
        (86400, 'Day'),
        (86400 * 7, 'Week'),
        (86400 * 30, 'Month'),
        (3600 * 6, '6 Hours'),
        (5, 'Dev'),
    )
    PRIORITY = (
        (1, 'Very High'),
        (2, 'High'),
        (3, 'Normal'),
        (4, 'Low'),
    )
    level = models.IntegerField(_('Level'), choices=LEVELS, default=20)
    title = models.CharField(_('Title'), max_length=100, unique=True)
    slug = models.SlugField(primary_key=True)
    message = models.TextField(_('Message'))
    priority = models.IntegerField(_('Priority'), choices=PRIORITY, default=3)
    cookie_max_age = models.IntegerField(_('Cookie Maximum Age'), choices=COOKIE_MAX_AGES, default=86400)
    users_log = models.TextField(_('User Log'), blank=True)
    expire_time = models.DateTimeField(_('Expire On'))
    expired = models.BooleanField(_('Expired'))
    time = models.DateTimeField(_('Time'), auto_now_add=True)
    class Meta:
        ordering = ['priority', '-time']
        get_latest_by = 'time'

    def __unicode__(self):
        return self.message

    def cookie(self):
        return str('message_' + self.slug)

    def save(self, *args, **kwargs):
        if  self.slug:
            pass
        else:
            self.slug = slugify(self.title)
        return super(UpdateMessage, self).save(*args, **kwargs)


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        exclude = ('user')

class RecaptchaForm(forms.Form):
    recaptcha = ReCaptchaField(label = _('I need to know that you are not a robot or a script'), widget=ReCaptchaWidget())

