import webapp2
import cgi
import urlparse
import jinja2
import os
from Blogs import Blogs
from Comments import Comments
from UserLoggedin import UserLoggedIn
from google.appengine.ext import db
from google.appengine.api import users 

class rss(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
       template = JINJA_ENVIRONMENT.get_template('rss.html') 
       
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       blogid = urlparse.parse_qs(parsed_url.query)['blogId']
       
       login = 0
       user = ""
       username = ""
#       self.response.write(sessionId)

       user = users.get_current_user()
       
       
#       try:
#            user = UserLoggedIn.get_by_id(int(sessionId))
#            username = user.blogger.nickname()
#            login = 1
#       except db.BadKeyError:
#            login = 0
#       except NameError:
#            login = 0 
#       self.response.write(login) 
       if user:
            login = 1
            username = user.nickname()
       else:
            login = 0
            login_url = users.create_login_url(cur_url)
       logout_url = users.create_logout_url('/')          
       blogs = db.GqlQuery("SELECT * FROM Blogs WHERE ParentBlogId="+blogid[0]+" ORDER BY create_time DESC")
       
       title = []
       content = []
       tag1 = []
       tag2 = []
       tag3 = []
       tag4 = []
       tag5 = []
       ids = []
       
       for b in blogs:
            title.append("<title>"+b.title+"</title>")
            content.append("<content>"+b.content+"</content>")
            tag1.append("<tag1>"+b.tag1+"</tag1>")
            tag2.append("<tag2>"+b.tag2+"</tag2>")
            tag3.append("<tag3>"+b.tag3+"</tag3>")
            tag4.append("<tag4>"+b.tag4+"</tag4>")
            tag5.append("<tag5>"+b.tag5+"</tag5>")
            id = b.key().id()
            ids.append("<postid>"+str(id)+"</postid>")
       blog_base = "<blog>"
       blog_end = "</blog>" 
       post_base = "<post>"
       post_end = "</post"       
       
       bloginxml = zip(ids,title,content,tag1,tag2,tag3,tag4,tag5)
       
       template_values = {'bloginxml' : bloginxml,
                          'login' : login,
                          'cur_url' : cur_url,
                          'username' : username,
 #                         'sessionId' : sessionId,
                          'blog_base' : blog_base, 
                          'blog_end' : blog_end,  
                          'post_base' : post_base, 
                          'post_end' : post_end,  
                          }
       
       self.response.write(template.render(template_values))
       
application = webapp2.WSGIApplication([
    ('/rss.*', rss)
    ], debug=True)

