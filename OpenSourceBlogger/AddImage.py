import webapp2
import jinja2
import os
import urlparse
from Images import Images
from google.appengine.ext import db
from google.appengine.api import users 
from google.appengine.api import images
from UserLoggedin import UserLoggedIn
from google.appengine.ext import blobstore

class AddImage(webapp2.RequestHandler):

    def get(self):
        JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
        template = JINJA_ENVIRONMENT.get_template('AddImage.html')
        
        cur_url = self.request.url
        parsed_url = urlparse.urlparse(cur_url)
        page_name = ""
        try:
            pn = urlparse.parse_qs(parsed_url.query)['PageName']
            page_name = int(pn[0])
        except Exception:
            pn = ""
        bi = urlparse.parse_qs(parsed_url.query)['blogId']
        cal = urlparse.parse_qs(parsed_url.query)['caller']        
        
        blogId = bi[0]
        caller = cal[0]
        login = 0
        login_url = ""
        username = ""
                  
#        if sessionId != 0:
#           login = 1
#           user = UserLoggedIn.get_by_id(int(session[0]))
#           username = user.blogger.nickname()
#        else: 
#           login = 0
#           login_url = users.create_login_url('/')
#        logout_url = users.create_logout_url('/')

        user = users.get_current_user()

        if user:
            login = 1
            username = user.nickname()
        else:
            login = 0
            login_url = users.create_login_url(cur_url)
        logout_url = users.create_logout_url('/')
    
        upload_url = blobstore.create_upload_url('/AddImageToStore.py')    
        
        query = "SELECT * from Images WHERE owner='"+username+"'"
        image_list = db.GqlQuery(query)
        
  #      self.response.write(cur_url)
                   
    #        image_urls.append(i_url)
    #        self.response.write(i_url)
      
    
        template_values = {'login' : login,
                          'login_url' : login_url,
                          'logout_url' : logout_url,
                          'username' : username,
                          'parentPageId' : page_name,
                          'image_list' : image_list,
                          'upload_url' : upload_url,
                          'blogId' : blogId,
                          'cur_url': cur_url,
                          'caller' : caller
                         }
                
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/AddImage.*', AddImage)
    ], debug=True)

