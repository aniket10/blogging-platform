import cgi  
import webapp2
import urlparse
import re
from datetime import datetime
from google.appengine.ext import db
from Blogs import Blogs


class UpdateBlogToDataStore(webapp2.RequestHandler):

    def get(self):
       form = cgi.FieldStorage()
       
       blogid = form['blogid'].value
       b = Blogs.get_by_id(int(blogid))
       
       form_title = form['title'].value
       form_content = form['content'].value
       form_tags = form['tags'].value
       form_modify_time = datetime.now()
       form_owner = form['owner'].value
       tags = form_tags.split(';')
       count_tags=len(tags)
       
       #newcntnt = re.sub(r'(https?://[^\s]+)',r"<a href='\1'>\1</a>",form_content)
        #newcntnt = re.sub(r'(https?://[^\s]+\.(jpg|gif|png)$)',r"<img src='\1' width='42'>",cntnt)
       #blgcntnt = re.sub(r'<a href=\'([^\']+\.(jpg|gif|png)$)\'>\1</a>',r"<img src='\1' width='42'>",newcntnt)
       
#       r = re.compile(r"(https?://[^ ]+)")
#       link_content = r.sub(r'<a href="\1">\1</a>', form_content)

       newcntnt = re.sub(r'(https?://[^\s]+\.(jpg|gif|png)$)',r'<img src=\1 width=500 height=300></img>',form_content)
       
       while count_tags <=5:
            tags.append("")
            count_tags = count_tags + 1
       
          
       b.title = form_title 
       b.content = newcntnt
       b.modify_time = form_modify_time
       b.tag1 = tags[0]
       b.tag2 = tags[1]
       b.tag3 = tags[2]
       b.tag4 = tags[3]
       b.tag5 = tags[4]
       b.put()
       self.redirect('/', False, False, None, None)
       
application = webapp2.WSGIApplication([
    ('/UpdateBlogToDataStore.*',UpdateBlogToDataStore)
    ], debug=True)



