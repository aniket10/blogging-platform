import webapp2
import urllib2
from putLink import putLink

class Convert(webapp2.RequestHandler):
    def convert(matchobj):
        url=matchobj.match(0)        
        response= urllib2.urlopen(HeadRequest(url))
        maintype= response.headers['Content-Type'].split(';')[0].lower()
        if maintype not in ('image/png', 'image/jpeg', 'image/gif'):
            return "<a href='"+link+"'>"+link+"</a>"
        else:
            return "<img src='"+link+"'></img>"

application = webapp2.WSGIApplication([
    ('/Convert.*', Convert)
    ], debug=True)