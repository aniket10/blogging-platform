import cgi  
import webapp2
import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Blogs(db.Model):
    title = db.StringProperty(required = True)
    content = db.StringProperty(required = True)
    blog_time = db.DateProperty()
    tags = db.StringProperty()
      


class InsertBlogToDataStore(webapp2.RequestHandler):

    def get(self):
       self.response.headers['Content-Type'] = 'text/html'
       self.response.write('<html><body><h1>Open Source Blogger</h1><hr>')
       self.response.write('<h3>Saving Blog ...</h3>')
       form = cgi.FieldStorage()
       
       form_title = form['title'].value
       form_content = form['content'].value
       form_tags = form['tags'].value
       form_blog_time = datetime.datetime.now().date();
       
       b = Blogs(title = form_title, 
                content = form_content,
                blog_time = form_blog_time,
                tags = form_tags)
       b.put()
       self.redirect('NewBlog.py;', False, False, Node, Node)
       self.response.write('</body></html>')



application = webapp2.WSGIApplication([
    ('/InsertBlogToDataStore.*',InsertBlogToDataStore)
    ], debug=True)



