import cgi  
import webapp2
import datetime
from Blogs import Blogs

      


class InsertBlogToDataStore(webapp2.RequestHandler):

    def get(self):
       self.response.headers['Content-Type'] = 'text/html'
       self.response.write('<html><body><h1>Open Source Blogger</h1><hr>')
       self.response.write('<h3>Saving Blog ...</h3>')
       form = cgi.FieldStorage()
       
       form_title = form['title'].value
       form_content = form['content'].value
       form_tags = form['tags'].value
       form_create_time = datetime.datetime.now().time()
       form_modify_time = datetime.datetime.now().time()
       form_owner = form['owner'].value
       tags = form_tags.split(';')
       count_tags=len(tags)
       
       while count_tags <=5:
            tags.append("")
            count_tags = count_tags + 1
       
       
       b = Blogs(owner = form_owner,
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



