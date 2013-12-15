import cgi  
import webapp2
import urlparse
from UserLoggedin import UserLoggedIn
from google.appengine.api import users
from google.appengine.ext import db

class login(webapp2.RequestHandler):

    def get(self):    
       form = cgi.FieldStorage()
       
#       cur_url = self.request.url
       cur_url = form['cur_url'].value
#       self.response.write(cur_url)
       self.redirect(users.create_login_url(cur_url))


       #login_url = users.create_login_url(cur_url)
       #self.redirect(cur_url, False, False, None, None)
 #      user = users.get_current_user()
              
 #      if user:
 #          u = UserLoggedIn(blogger = user)
 #          u.put()
 #          sessionId = str(u.key().id())
               
  #         iplen = len(target_url)
  #         substr_len = iplen-1
  #         target_substr = target_url[:substr_len]    
  #         url = target_substr+""+sessionId
  #         self.redirect(url, False, False, None, None)
  #     else:
              
       
              

application = webapp2.WSGIApplication([
    ('/login.*',login)
    ], debug=True)



