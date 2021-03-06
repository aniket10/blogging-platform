import webapp2
import cgi
import jinja2
import urlparse
import os
import re
import urllib2
import urllib
import htmllib
from Blogs import Blogs
from Comments import Comments
from UserLoggedin import UserLoggedIn
from Follow import Follow
from Pages import Pages
from google.appengine.ext import db
from putLink import putLink
from google.appengine.api import users
#from Convert import Convert

#class Convert(webapp2.RequestHandler):
def convert(matchobj):
    url=matchobj.group(0)        
    try:
        response= urllib2.urlopen(putLink(url))
    except Exception:
        return "<a href='"+url+"'>"+url+"</a>"
    maintype= response.headers['Content-Type'].split(';')[0].lower()
    if maintype not in ('image/png', 'image/jpeg', 'image/gif'):
        return "<a href='"+url+"'>"+url+"</a>"
    else:
        return "<img src='"+url+"' width='500' height='250'></img>"

class BlogFeed(webapp2.RequestHandler):

    def get(self):
       print "Content-Type: text/html" 
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=False)
       template = JINJA_ENVIRONMENT.get_template('BlogFeed.html')
       
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       pageNo = urlparse.parse_qs(parsed_url.query)['page']
       query_name = urlparse.parse_qs(parsed_url.query)['query']
       type_name = urlparse.parse_qs(parsed_url.query)['type']
#       session_name = urlparse.parse_qs(parsed_url.query)['sessionId']
       page = int(pageNo[0])
       query = query_name[0]
       type = type_name[0]
#       sessionId = session_name[0]   
       blogs = []
       parentId = []
       blog_owner = ''
       content = []
       blog_name = ""
              
       query_type = 0
       
       if type == 'owner':
           blog_owner = query
           blogs = db.GqlQuery("SELECT * FROM Blogs WHERE owner = '"+blog_owner+"' ORDER BY create_time DESC")
       
           query_type = 0
       elif type == 'tags':
           query_type = 1
           all_blogs = db.GqlQuery('SELECT * from Blogs ORDER BY create_time DESC')
           blogs = []
           for b in all_blogs:
               if query in [b.tag1,b.tag2,b.tag3,b.tag4,b.tag5]:
                   blogs.append(b)
           
           if len(blogs) == 0:
               self.redirect('/', False, False, None, None)
       elif type == 'blog':
            self.redirect('viewAllBlogs.py?name='+query, False, False, None, None) 
       elif type == 'sblog':
            query_type = 2            
            blogs = db.GqlQuery("SELECT * FROM Blogs WHERE ParentBlogId="+query+" ORDER BY create_time DESC")
            blogpage = Pages.get_by_id(int(query))
            blog_name = blogpage.page_name
            
       likes = []
       comments= []
       tags = []
                  
       more = 0
       count = -1
       selected = 0
       per_page = 10
       subset_blogs = []
       blogsnlikes = []
       login = 0
       user = ""
       username = ""
       
       user = users.get_current_user()
       
 #      try:
 #           user = UserLoggedIn.get_by_id(int(sessionId))
 #           username = user.blogger.nickname()
 #           login = 1
 #      except db.BadKeyError:
 #           login = 0
  
       if user:
            login = 1
            username = user.nickname()
       else:
            login = 0
            login_url = users.create_login_url(cur_url)      
       following = 0
       
       dbquery = "Select * from Follow where item='"+query+"' AND user='"+username+"' AND type="+str(query_type)
       follow_list = db.GqlQuery(dbquery)
       follow_count = 0
       
       for f in follow_list:
           follow_count = follow_count + 1
           
       if follow_count > 0:
            following = 1
       
 #      count_blogs = count(blogs)
       for b in blogs:
           if b.tag1 not in tags:
               tags.append(b.tag1)
           
           if b.tag2 not in tags:
               tags.append(b.tag2)
               
           if b.tag3 not in tags:
               tags.append(b.tag3)
               
           if b.tag4 not in tags:
               tags.append(b.tag4)
               
           if b.tag5 not in tags:
               tags.append(b.tag5) 
 
       for b in blogs:
           count = count + 1
           if (page-1)*per_page > count:
               continue
           selected = selected + 1
           blogid = str(b.key().id())
           query_string = "SELECT * FROM Comments WHERE blogid ='"+blogid+"'"
           like_count = db.GqlQuery(query_string)
#           lc = Likes.filter('blogid=',blogid).get().count()
           count_likes = 0 
           for lc in like_count:
               count_likes = count_likes + 1
#           self.response.write(count_likes) 
           likes.append(str(count_likes))
           subset_blogs.append(b)
#           self.response.write(b.title)
           text_content = unicode(b.content, "utf8")
  #         self.response.write(text_content)
           
           
           #\bhttps?://\w*\b(?<!(png|jpg|gif))
           #r = re.compile(r"(https?://[^\s]+)")
           #c = Convert();
           link_content = re.sub(r'(https?://[^\s]+)',convert,text_content)
#          self.response.write(link_content)
           content.append(link_content)  
           if selected == per_page:
       #        if count != count_blogs:
               more = 1
               break    
#       self.response.write(likes)    
       blogsnlikes = zip(subset_blogs,likes,content)
#       self.response.write(blogsnlikes)
 #      self.response.write(cur_url)
       template_values = {
#                          'blogs': subset_blogs,
                          'blogsnlikes':blogsnlikes,
                          'blog_owner': blog_owner,
                          'more':more,
                          'nextpage':page+1,
                          'query': query,
                          'type':type,
                          'query_type' : query_type,
                          'username' : username,
#                          'sessionId' :sessionId,
                          'cur_url' : cur_url,
                          'following' : following,
                          'parentId' : parentId,
                          'login' : login,
                          'blogname' : blog_name,
                          'tags' : tags
#                          'likes':likes
                          }
              
       self.response.write(template.render(template_values))      

application = webapp2.WSGIApplication([
    ('/BlogFeed.*', BlogFeed)
    ], debug=True)

