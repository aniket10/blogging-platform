import cgi  
import webapp2
import re
from datetime import datetime
from Blogs import Blogs
from TempStore import TempStore 
from google.appengine.ext import db
from Images import Images
from UserLoggedin import UserLoggedIn
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.api import images


class AddImageToStore(blobstore_handlers.BlobstoreUploadHandler):
#class AddImageToStore(webapp2.RequestHandler):

    def post(self):
       form_image = self.get_uploads('newImage')
    
       blogId = self.request.get('blogId')
       caller = self.request.get('caller')
       self.response.out.write('<html><body>You wrote:<pre>')
       self.response.out.write(cgi.escape(self.request.get('PageName')))
       self.response.out.write('</pre></body></html>')
       
       username = ""
#       try:
#            user = UserLoggedIn.get_by_id(int(sessionId))
#            username = user.blogger.nickname()
#            login = 1
#       except db.BadKeyError:
#            login = 0

       user = users.get_current_user()

       if user:
           login = 1
           username = user.nickname()
       else:
           login = 0
           login_url = users.create_login_url(cur_url)
       logout_url = users.create_logout_url('/')
        
       form_owner = username            
    
       blob_info = form_image[0]
       im_key = blob_info.key()
       im_url = images.get_serving_url(blob_info.key())
      
       i = Images(owner = form_owner,
                  image_url = im_url,
                  image_key = str(im_key))
       
       target_url = "/AddImage.py?blogId="+blogId+"&caller="+caller
       i.put()
       self.redirect(target_url, False, False, None, None)
       
       self.response.write('</body></html>')



application = webapp2.WSGIApplication([
    ('/AddImageToStore.*',AddImageToStore)
    ], debug=True)



