import cgi  
import webapp2
import re
from datetime import datetime
from Blogs import Blogs
from TempStore import TempStore 


class InsertBlogToDataStore(webapp2.RequestHandler):

    def get(self):
       form = cgi.FieldStorage()
       
       #self.response.write(form['action'].value)
       action = form['action'].value 
       
       blogId = form['blogId'].value
       image_url = form['image'].value
       
       b = TempStore.get_by_id(int(blogId))
       
       b.content.append(' '+image_url)
       
       b.put()

       self.response.write("Added to tempstore")
       self.redirect('/NewBlog.py?blogId='+str(blogId)+'&parentPageId=0', False, False, None, None)
       

application = webapp2.WSGIApplication([
    ('/InsertBlogToDataStore.*',InsertBlogToDataStore)
    ], debug=True)



