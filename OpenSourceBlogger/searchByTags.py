import webapp2
import cgi
import jinja2
import urlparse
import os
from Blogs import Blogs

from google.appengine.ext import db

class searchByTags(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
       template = JINJA_ENVIRONMENT.get_template('BlogFeed.html')
        
       
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       pageNo = urlparse.parse_qs(parsed_url.query)['page']
       tag_name = urlparse.parse_qs(parsed_url.query)['query']
       page = int(pageNo[0])  
       tag = tag_name[0]

#       blogs = db.GqlQuery("SELECT * FROM Blogs WHERE tag1 ='"+tag+"' or tag2 ='"+tag+"' or tag3 ='"+tag+"' or tag4 ='"+tag+"' or tag5 ='"+tag+"' ORDER BY blog_time DESC")
 #      def blogs = search.search {SELECT ALL FROM Blogs
#       blogs = db.GqlQuery("SELECT * FROM Blogs WHERE '"+tag+"' in [tag1,tag2,tag3,tag4,tag5] 'ORDER BY blog_time DESC")
 #                                 SORT DESC BY blog_time
 #                                 WHERE tags =~ tag
 #                                 }

       blogs = Blogs.query().filter(ndb.OR(tag1 == tag ,tag2 == tag))
                     
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
    ('/searchByTags.*', searchByTags)
    ], debug=True)

