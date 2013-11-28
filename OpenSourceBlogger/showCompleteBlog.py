import webapp2
import cgi
import urlparse
from Blogs import Blogs
from google.appengine.ext import db

class showCompleteBlog(webapp2.RequestHandler):

    def get(self):
       self.response.headers['Content-Type'] = 'text/html'
       self.response.write('<html><body><h1>Open Source Blogger</h1><hr>')
       
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       blogid = urlparse.parse_qs(parsed_url.query)['blogid']
       
 #      blogs = db.GqlQuery("SELECT * FROM Blogs WHERE ID = '"+blogid[0]+"'")
       
  #     for b in blogs:
  
       b = Blogs.get_by_id(int(blogid[0]))
       self.response.write('<h1>Blogs by '+b.owner)
       self.response.write('</h1>')
       self.response.write('<hr>')
       self.response.write('<h3>'+b.title+'</h3>')
       self.response.write('<h5>'+str(b.blog_time)+'</h5>')
       self.response.write(b.content)
       self.response.write('<br>')
           
       self.response.write('</body></html>')

application = webapp2.WSGIApplication([
    ('/showCompleteBlog.*', showCompleteBlog)
    ], debug=True)

