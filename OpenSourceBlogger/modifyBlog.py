import webapp2
import cgi
import urlparse
import jinja2
import os
from Blogs import Blogs
from Comments import Comments
from google.appengine.ext import db
from google.appengine.api import users 
from TempStore import TempStore     

class modifyBlog(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
       template = JINJA_ENVIRONMENT.get_template('modifyBlog.html') 
       
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       bid = urlparse.parse_qs(parsed_url.query)['blogId']
       blogid = int(bid[0])
       caller = 0
 #      self.response.write(cur_url)
   
       
       content = ""
       tags = ""
       title = ""
  #     self.response.write('caller=')
  #     self.response.write(caller)
       
#       sessionid = urlparse.parse_qs(parsed_url.query)['sessionId']   
       b = Blogs.get_by_id(blogid)
       
       try:
           id = b.key().id()
           content = unicode(b.content, "utf8")
       except Exception :
   #        self.response.write('caller = 1')
           t = TempStore.get_by_id(blogid)
           blogid = int(t.blogId)     
           content = unicode(t.content, "utf8")
           tags = t.tag
           title = t.title
           caller = 1
           t.delete()
           b = Blogs.get_by_id(blogid)
       query = "SELECT * FROM Comments WHERE blogid='"+str(blogid)+"'"
       comments_list = db.GqlQuery(query)
       count_comments = 0
       for c in comments_list:
           count_comments = count_comments + 1
       
  #     self.response.write(b.key().id())
  #     self.response.write(blogid)
    #   self.response.write(t.blogId)
       login =0
#       if int(sessionid[0]) != 0:
#           login = 1
#       else:
#           login = 0      
 
       user = users.get_current_user()
       
       if user:
            login = 1
            username = user.nickname()
       else:
            login = 0
            login_url = users.create_login_url(cur_url)
       logout_url = users.create_logout_url('/') 
       
       template_values = {'comments':comments_list,
                          'b': b,
                          'comment_count':count_comments,
 #                         'sessionId' : sessionid[0],
                          'login' : login,
                          'caller' : caller,
                          'tags' : tags,
                          'title' : title,
                          'content' : content
                          }
       
       self.response.write(template.render(template_values))
       
application = webapp2.WSGIApplication([
    ('/modifyBlog.*', modifyBlog)
    ], debug=True)

