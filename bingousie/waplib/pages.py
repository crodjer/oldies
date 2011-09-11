from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
import app


try:
    if app.OPENID_PROVIDERS: OPENID_PROVIDERS=app.OPENID_PROVIDERS
except:
    OPENID_PROVIDERS = [
        {'name': 'Google',  'url': 'google.com/accounts/o8/id'},
        {'name': 'Yahoo',   'url': 'yahoo.com'},
        {'name': 'AOL',     'url': 'aol.com'},
        {'name': 'MyOpenID','url': 'myopenid.com'},
        # add more here
    ]

class BasePage(webapp.RequestHandler):
    def __init__(self):
        self.user = users.get_current_user()
        self.template_vars = {
                'user': self.user,
                'environ': self,
            }

    def setup(self):
        self.template_vars['logout_url'] = users.create_logout_url(self.request.url)
        self.template_vars['openid_providers'] = self.openid_providers()
        self.template_vars['request']=self.request

    def get(self, *args, **kwargs):
        self.setup()
        self.DoGet(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.setup()
        self.DoPost(*args, **kwargs)

    def DoGet(self):
        pass
    def DoPost(self):
        pass

    def render_template(self, template_name, values = None, *args, **kwargs):
        if values:
            for value in values:  self.template_vars[value] = values[value]
        self.response.out.write(template.render(app.TEMPLATE_PATH+template_name, self.template_vars, *args, **kwargs))

    def openid_providers(self):
        for p in OPENID_PROVIDERS:
            p['login_url'] = users.create_login_url(self.request.get('next', '/') , p['name'], p['url'])
        return OPENID_PROVIDERS
