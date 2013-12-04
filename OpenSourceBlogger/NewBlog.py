import webapp2
import jinja2
import os
import urlparse
from google.appengine.api import users 
from UserLoggedin import UserLoggedIn

class MainPage(webapp2.RequestHandler):

    def get(self):
        JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
        template = JINJA_ENVIRONMENT.get_template('NewBlog.html')
        
        cur_url = self.request.url
        parsed_url = urlparse.urlparse(cur_url)
        session = urlparse.parse_qs(parsed_url.query)['sessionId']  
        sessionId = int(session[0])
       
        login = 0
        login_url = ""
        username = ""
                  
        if sessionId != 0:
           login = 1
           user = UserLoggedIn.get_by_id(int(session[0]))
           username = user.blogger.nickname()
        else: 
           login = 0
           login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
    
        template_values = {'login' : login,
                          'login_url' : login_url,
                          'logout_url' : logout_url,
                          'username' : username,
                          'sessionId' : session,
                            }
                
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/NewBlog.*', MainPage)
    ], debug=True)

