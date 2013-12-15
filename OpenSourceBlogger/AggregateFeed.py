import webapp2
import cgi
import jinja2
import urlparse
import os
from Blogs import Blogs
from Comments import Comments
from UserLoggedin import UserLoggedIn
from Follow import Follow
from google.appengine.ext import db

class BlogFeed(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
       template = JINJA_ENVIRONMENT.get_template('BlogFeed.html')
       
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       pageNo = urlparse.parse_qs(parsed_url.query)['page']
       query_name = urlparse.parse_qs(parsed_url.query)['query']
       type_name = urlparse.parse_qs(parsed_url.query)['type']
       session_name = urlparse.parse_qs(parsed_url.query)['sessionId']
       page = int(pageNo[0])
       query = query_name[0]
       type = type_name[0]
       sessionId = session_name[0]   
       blogs = []
       blog_owner = ''
              
       query_type = 0
       
       if type == 'owner':
           blog_owner = query
           blogs = db.GqlQuery("SELECT * FROM Blogs WHERE owner = '"+blog_owner+"' ORDER BY create_time DESC")
       
           query_type = 0
       else:
       
           query_type = 1
           all_blogs = db.GqlQuery('SELECT * from Blogs')
           blogs = []
           for b in all_blogs:
               if query in [b.tag1,b.tag2,b.tag3,b.tag4,b.tag5]:
                   blogs.append(b)
           
           if len(blogs) == 0:
               self.redirect('/', False, False, None, None)
       likes = []
       comments= []
                  
       more = 0
       count = -1
       selected = 0
       per_page = 2
       subset_blogs = []
       blogsnlikes = []
       user = UserLoggedIn.get_by_id(int(sessionId))
       username = user.blogger.nickname()
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
           if selected == per_page:
       #        if count != count_blogs:
               more = 1
               break    
#       self.response.write(likes)    
       blogsnlikes = zip(subset_blogs,likes)
#       self.response.write(blogsnlikes)
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
                          'sessionId' :sessionId,
                          'cur_url' : cur_url,
                          'following' : following
#                          'likes':likes
                          }
              
       self.response.write(template.render(template_values))
           
application = webapp2.WSGIApplication([
    ('/BlogFeed.*', BlogFeed)
    ], debug=True)

