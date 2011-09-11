from google.appengine.ext import webapp

register = webapp.template.create_template_register()

def in_list(var, list):
    if var in list: return True
    else: return False
    
register.filter(in_list)    