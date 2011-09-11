import os
import main
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

OPENID_PROVIDERS = [
    {'name': 'Google',  'url': 'google.com/accounts/o8/id'},
    {'name': 'Yahoo',   'url': 'yahoo.com'},
    {'name': 'AOL',     'url': 'aol.com'},
    {'name': 'MyOpenID','url': 'myopenid.com'},
    # add more here
]

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates/')

webapp.template.register_template_library('templatelib')
application = webapp.WSGIApplication([
    ('/', main.MainPage),
    ('/new/', main.NewGame),
    ('/tablegen/', main.TableGen),
    ('/cleanup/', main.CleanUp),
    ('/(?P<id>\d+)/', main.GamePage),
    ('/(?P<id>\d+)/gennumber/', main.GenNumber),
    ('/(?P<id>\d+)/ajaxnum/', main.GenNumberAJAX),
    ('/login/', main.LoginPage),
    ], debug=True)

def main():
    run_wsgi_app(application)
if __name__ == "__main__":
    main()
