import cgi  
import webapp2
import urlparse
from UserLoggedin import UserLoggedIn
from google.appengine.api import users


class logout(webapp2.RequestHandler):

    def get(self):    
#       form = cgi.FieldStorage()
       
#       sessionId = form['sessionId'].value
              
#       s = UserLoggedIn.get_by_id(int(sessionId))
#       username = s.blogger
#       s.delete()
       
       
       url = users.create_logout_url('/')
       
  #     self.response.write("You have Logged Out")
       self.redirect(url, False, False, None, None)



application = webapp2.WSGIApplication([
    ('/logout.*',logout)
    ], debug=True)



