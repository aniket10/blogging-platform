import cgi  
import webapp2
import urlparse
from UserLoggedin import UserLoggedIn
from google.appengine.api import users
from google.appengine.ext import db

class login(webapp2.RequestHandler):

    def get(self):    
       form = cgi.FieldStorage()
       
       cur_url = self.request.url
       target_url = form['cur_url'].value
       
       login_url = users.create_login_url(cur_url)
       
       user = users.get_current_user()
              
       if user:
           u = UserLoggedIn(blogger = user)
           u.put()
           sessionId = str(u.key().id())
               
           iplen = len(target_url)
           substr_len = iplen-1
           target_substr = target_url[:substr_len]    
           url = target_substr+""+sessionId
           self.redirect(url, False, False, None, None)
       else:
           self.redirect(login_url, False, False, None, None)       
       
              

application = webapp2.WSGIApplication([
    ('/login.*',login)
    ], debug=True)



