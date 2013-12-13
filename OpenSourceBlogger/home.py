import webapp2
import cgi
import urlparse
import jinja2
import os
import re
from Blogs import Blogs
from google.appengine.ext import db
from google.appengine.api import users
from UserLoggedin import UserLoggedIn
from Comments import Comments
from Follow import Follow
from Pages import Pages

class home(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=False)
       template = JINJA_ENVIRONMENT.get_template('home.html') 
    
       user = users.get_current_user()
       
       login = 0
       login_url = ""
       username = ""
       sessionId = 0
       display_list = []
       comments = []
       content = []
              
       if user:
           login = 1
           username = user.nickname()
           
           dbquery = "SELECT * FROM UserLoggedIn WHERE blogger=:1",user
           userEntry = db.GqlQuery("SELECT * FROM UserLoggedIn WHERE blogger=:1",user)
           
           entryCount = 0
           for ue in userEntry:
               sessionId= ue.key().id()
               entryCount = entryCount + 1
           
           if entryCount == 0:
               u = UserLoggedIn(blogger = user)
               u.put()
               sessionId = str(u.key().id())
           
           dbquery = "SELECT * FROM Follow WHERE user='"+username+"'"
           follow_list = db.GqlQuery(dbquery)
           
           blogs = []
           ppl = []
           tags = []
           
           for f in follow_list:
               self.response.write(f.item)
               if f.type == 0:
                   self.response.write('type = 0')
                   ppl.append(f.item)
               if f.type == 1:
                   self.response.write('type = 1')
                   tags.append(f.item)
               if f.type == 2:
                   self.response.write('type = 2')
                   blogs.append(int(f.item))    
           
           dbquery = "SELECT * FROM Blogs ORDER BY modify_time DESC"
           blog_list = db.GqlQuery(dbquery)
           
           selected_count = 0
           content = []
           
           self.response.write(blogs)
           
           for b in blog_list:
               self.response.write("---")
               self.response.write(b.key().id())
               self.response.write(b.ParentBlogId)
               selected = 0
               if b.owner in ppl:
                   display_list.append(b)
                   selected = 1
               elif b.tag1 in tags:
                   display_list.append(b)
                   selected = 1
               elif b.tag2 in tags:
                   display_list.append(b)
                   selected = 1
               elif b.tag3 in tags:
                   display_list.append(b)
                   selected = 1
               elif b.tag4 in tags:
                   display_list.append(b)
                   selected = 1
               elif b.tag5 in tags:    
                   display_list.append(b)
                   selected = 1
               elif b.ParentBlogId in blogs:
                   self.response.write('matching parent blogid')
                   display_list.append(b)
                   selected = 1 
               if selected == 1:
                   selected_count = selected_count + 1    
                   blogid = str(b.key().id())
                   query_string = "SELECT * FROM Comments WHERE blogid ='"+blogid+"'"
                   comment_count = db.GqlQuery(query_string)
#           lc = Likes.filter('blogid=',blogid).get().count()
                   count_comment = 0 
                   for cc in comment_count:
                       count_comment = count_comment + 1
#           self.response.write(count_likes) 
                   comments.append(str(count_comment))
                   r = re.compile(r"([^(<img src=)].https?://[^ ]+)")
                   link_content = r.sub(r'<a href="\1">\1</a>', b.content)
                   content.append(link_content)
                   if selected_count == 100:
                       break
                   
           self.response.write(selected_count)
       else: 
           login = 0
           login_url = users.create_login_url('/')
       logout_url = "logout.py?sessionId="+str(sessionId)
                 
       dlc = zip(display_list,comments,content)
       userblogs = []
       dbquery = "SELECT * FROM Pages WHERE owner = '"+username+"'";
       userblogs = db.GqlQuery(dbquery)
       
       ubcount = 0
       for ub in userblogs:
           ubcount = ubcount + 1
           
       cur_url = self.request.url
       
       template_values = {'login' : login,
                          'login_url' : login_url,
                          'logout_url' : logout_url,
                          'username' : username,
                          'sessionId' : sessionId,
                          'display_listnComments' : dlc,
                          'userblogs' : userblogs,
                          'ubcount' : ubcount,
                          'cur_url' : cur_url
                           }                          
       self.response.write(template.render(template_values))
       
application = webapp2.WSGIApplication([
    ('/', home)
    ], debug=True)

