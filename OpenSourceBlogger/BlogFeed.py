import webapp2
import cgi
from Blogs import Blogs
from google.appengine.ext import db

class BlogFeed(webapp2.RequestHandler):

    def get(self):
       self.response.headers['Content-Type'] = 'text/html'
       self.response.write('<html><body><h1>Open Source Blogger</h1><hr>')
       blog_owner = 'aniket'
       
       blogs = db.GqlQuery("SELECT * FROM Blogs WHERE owner = '"+blog_owner+"' ORDER BY blog_time DESC")
       
       self.response.write('<h1>Blogs by '+blog_owner)
       self.response.write('</h1>')
       for b in blogs:
           self.response.write('<hr>')
           self.response.write('<h3>'+b.title+'</h3>')
           self.response.write('<h5>'+str(b.blog_time)+'</h5>')
        
           len_content = len(str(b.content))
           if len_content <= 500:
               self.response.write(b.content)
           else :
               sub_content = b.content[:500]
               self.response.write(sub_content)
               blog_id = str(b.key().id())
               self.response.write('''&nbsp;&nbsp;&nbsp;<a href=showCompleteBlog.py?blogid='''+blog_id+'''>more</a>''')
           self.response.write('<br>')
       
       self.response.write('</body></html>')

application = webapp2.WSGIApplication([
    ('/BlogFeed.*', BlogFeed)
    ], debug=True)

