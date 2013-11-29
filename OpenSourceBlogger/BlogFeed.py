import webapp2
import cgi
import jinja2
import urlparse
import os
from Blogs import Blogs
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
       page = int(pageNo[0])
       query = query_name[0]
       type = type_name[0]   
       blogs = []
       blog_owner = ''
       
       if type == 'owner':
           blog_owner = query
           blogs = db.GqlQuery("SELECT * FROM Blogs WHERE owner = '"+blog_owner+"' ORDER BY blog_time DESC")
       else:
           self.redirect('/', False, False, None, None)
           
       likes = []
       comments= []
       
       more = 0
       count = -1
       selected = 0
       per_page = 2
       subset_blogs = []
 #      count_blogs = count(blogs)
       for b in blogs:
           count = count + 1
           if (page-1)*per_page > count:
               continue
           selected = selected + 1
           blogid = str(b.key().id())
           query_string = "SELECT * FROM LIKES WHERE blogid ='"+blogid+"'"
           like_count = db.GqlQuery(query_string)
           for lc in like_count:
               likes.append(str(lc))
           subset_blogs.append(b)
           if selected == per_page:
       #        if count != count_blogs:
               more = 1
               break
           
       template_values = {
                          'blogs': subset_blogs,
                          'blog_owner': blog_owner,
                          'more':more,
                          'nextpage':page+1,
                          'query':blog_owner,
                          'type':type,
                          'likes':likes
                          }
              
       self.response.write(template.render(template_values))
           
application = webapp2.WSGIApplication([
    ('/BlogFeed.*', BlogFeed)
    ], debug=True)

