import cgi  
import webapp2
from datetime import datetime
from Blogs import Blogs
from Follow import Follow

      


class AddFollow(webapp2.RequestHandler):

    def get(self):
       form = cgi.FieldStorage()
       
       form_item = form['item'].value
       form_user = form['user'].value
       form_type = int(form['type'].value)
       url = form['url'].value
       
       f = Follow(item = form_item,
                 user = form_user, 
                 type = form_type,
                 )
       f.put()
       self.redirect(url, False, False, None, None)



application = webapp2.WSGIApplication([
    ('/AddFollow.*',AddFollow)
    ], debug=True)



