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
        
       blog_owner = 'aniket'
       blogs = db.GqlQuery("SELECT * FROM Blogs WHERE owner = '"+blog_owner+"' ORDER BY blog_time DESC")
       
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       pageNo = urlparse.parse_qs(parsed_url.query)['page']
       page = int(pageNo[0])  
       
       more = 0
       count = -1
       selected = 0
       per_page = 2
       subset_blogs = []
       for b in blogs:
           count = count + 1
           if (page-1)*per_page > count:
               continue
           selected = selected + 1
           subset_blogs.append(b)
           if selected == per_page:
               more = 1
               break
           
       template_values = {
                          'blogs': subset_blogs,
                          'blog_owner': blog_owner,
                          'more':more,
                          'nextpage':page+1
                          }
              
       self.response.write(template.render(template_values))
           
application = webapp2.WSGIApplication([
    ('/BlogFeed.*', BlogFeed)
    ], debug=True)

