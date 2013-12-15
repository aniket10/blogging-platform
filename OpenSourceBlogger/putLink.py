import webapp2
import urllib2
class putLink(urllib2.Request):
    def get_method(self):
        return 'HEAD'

application = webapp2.WSGIApplication([
    ('/putLink.*', putLink),
    ], debug=True)