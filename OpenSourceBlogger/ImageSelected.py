import cgi  
import webapp2
import re
from datetime import datetime
from Blogs import Blogs
from TempStore import TempStore 


class ImageSelected(webapp2.RequestHandler):

    def get(self):
       form = cgi.FieldStorage()
       
       #self.response.write(form['action'].value)
       action = form['action'].value 
       
       blogId = form['blogId'].value
       image_url = form['image'].value
       caller = form['caller'].value
       
       b = TempStore.get_by_id(int(blogId))
       
       content_str = str(b.content)
       self.response.write(content_str)
        
       content_str= content_str+' '+image_url
       self.response.write(content_str)
       
       b.content = content_str  
       b.put()

       self.response.write("Added to tempstore")
       if caller == 0:
           self.redirect('/NewBlog.py?blogId='+str(blogId)+'&parentPageId=0', False, False, None, None)
       else:
           self.redirect('/modifyBlog.py?blogId='+str(blogId)+'&caller=1', False, False, None, None)

application = webapp2.WSGIApplication([
    ('/ImageSelected.*',ImageSelected)
    ], debug=True)



