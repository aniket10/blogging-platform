import webapp2
import jinja2
import os

class MainPage(webapp2.RequestHandler):

    def get(self):
        JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=True)
        template = JINJA_ENVIRONMENT.get_template('NewBlog.html')
        self.response.write(template.render())

application = webapp2.WSGIApplication([
    ('/NewBlog.*', MainPage)
    ], debug=True)

