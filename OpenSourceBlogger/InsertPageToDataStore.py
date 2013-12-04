import cgi  
import webapp2
from datetime import datetime
from Pages import Pages     


class InsertPageToDataStore(webapp2.RequestHandler):

    def get(self):
       form = cgi.FieldStorage()
       
       form_title = form['title'].value
       form_create_time = datetime.now().time()
       form_owner = form['owner'].value
    
       p = Pages(owner = form_owner,
                 page_name = form_title, 
                 create_time = form_create_time,
                 )
       p.put()
       self.redirect('/', False, False, None, None)
       



application = webapp2.WSGIApplication([
    ('/InsertPageToDataStore.*',InsertPageToDataStore)
    ], debug=True)



