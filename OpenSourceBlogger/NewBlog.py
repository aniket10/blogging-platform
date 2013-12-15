import webapp2
import jinja2
import os
import urlparse
from google.appengine.api import users 
from UserLoggedin import UserLoggedIn
from TempStore import TempStore

class MainPage(webapp2.RequestHandler):

    def get(self):
        JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
        template = JINJA_ENVIRONMENT.get_template('NewBlog.html')
        
        cur_url = self.request.url
        parsed_url = urlparse.urlparse(cur_url)
#        session = urlparse.parse_qs(parsed_url.query)['sessionId']
        pn = urlparse.parse_qs(parsed_url.query)['parentPageId']    
#        sessionId = int(session[0])
        page_name = int(pn[0])
        
        tags = ""
        title = ""
        content = ""
        
        type = 0  
        b = ""
        if page_name == 0 :
            bi = urlparse.parse_qs(parsed_url.query)['blogId']
            blogId = bi[0]
            
            b = TempStore.get_by_id(int(blogId))
            type = 1
            page_name = b.ParentBlogId
            title = b.title
            content = b.content
            tags = b.tag
            
            b.delete()
            
        login = 0
        login_url = ""
        username = ""
 
        user = users.get_current_user()
        
                  
#        if sessionId != 0:
#           login = 1
#           user = UserLoggedIn.get_by_id(int(session[0]))
#           username = user.blogger.nickname()
#        else: 
#           login = 0
#           login_url = users.create_login_url('/')
        if user:
            login = 1
            username = user.nickname()
        else:
            login = 0
            login_url = users.create_login_url(cur_url)
        logout_url = users.create_logout_url('/')
    
        template_values = {'login' : login,
                          'login_url' : login_url,
                          'logout_url' : logout_url,
                          'username' : username,
   #                       'sessionId' : sessionId,
                          'parentPageId' : page_name,
                          'type' : type,
                          'tags' : tags,
                          'content' : content,
                          'title' : title
                            }
                
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/NewBlog.*', MainPage)
    ], debug=True)

