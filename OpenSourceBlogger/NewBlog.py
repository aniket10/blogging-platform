import webapp2

class MainPage(webapp2.RequestHandler):

    def get(self):
       self.response.headers['Content-Type'] = 'text/html'
       self.response.write('<html><body><h1>Open Source Blogger</h1><hr>')
       self.response.write('<h3>Create New Blog</h3>')
       self.response.write('''<form name = 'newBlog' action='InsertBlogToDataStore.py' > ''')
       self.response.write('Title goes here:')
       self.response.write('''<input type='text' name='title' width='50px'/><br><br>''')
       self.response.write('Contents go here:<br>')
       self.response.write('''<textarea rows=15 cols=50 name='content'   ></textarea><br>''')
       self.response.write('<br>Enter tags seperated by ; (semi-colon):<br>')
       self.response.write('''<input type='text' name='tags'/><br><br>''')
       self.response.write('''<input type='submit' value='Create Blog'>''')
       self.response.write('</form>')
       self.response.write('</body></html>')

application = webapp2.WSGIApplication([
    ('/', MainPage)
    ], debug=True)

