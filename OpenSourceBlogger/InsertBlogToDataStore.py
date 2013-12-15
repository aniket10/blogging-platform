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
       
       form_title = form['title'].value
       form_content = form['content'].value
       try:
           form_tags = form['tags'].value
       except Exception:
            form_tags=""
       form_parent = form['parentPageId'].value
       form_create_time = datetime.now()
       form_modify_time = datetime.now()
       form_owner = form['owner'].value
#       sessionId = form['sessionId'].value
       tags = form_tags.split(';')
       count_tags=len(tags)
                         
       while count_tags <=5:
            tags.append("")
            count_tags = count_tags + 1
           
           
       if action == "Add Picture":
            t = TempStore(ParentBlogId = int(form_parent),
                          owner = form_owner,
                          title = form_title, 
                          content = form_content,                
                          tag = form_tags
                          )
            t.put()
            id = t.key().id()
            self.response.write("Added to tempstore")
            self.redirect('/AddImage.py?blogId='+str(id)+'&PageName='+str(form_parent)+'&caller=0', False, False, None, None)
       if action == "Create Blog Post":    
           b = Blogs(ParentBlogId = int(form_parent),
                     owner = form_owner,
                     title = form_title, 
                     content = form_content,
                     create_time = form_create_time,
                     modify_time = form_modify_time,
                     tag1 = tags[0],
                     tag2 = tags[1],
                     tag3 = tags[2],
                     tag4 = tags[3],
                     tag5 = tags[4])
           b.put()
           self.redirect('/', False, False, None, None)
       self.response.write('</body></html>')



application = webapp2.WSGIApplication([
    ('/InsertBlogToDataStore.*',InsertBlogToDataStore)
    ], debug=True)



