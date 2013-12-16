import webapp2
import cgi
import urlparse
import jinja2
import os
import re
import urllib2
import urllib
import htmllib
from Blogs import Blogs
from Comments import Comments
from UserLoggedin import UserLoggedIn
from google.appengine.ext import db
from putLink import putLink
from google.appengine.api import users
#from Convert import Convert

#class Convert(webapp2.RequestHandler):
def convert(matchobj):
    url=matchobj.group(0)        
    try:
        response= urllib2.urlopen(putLink(url))
    except Exception:
        return "<a href='"+url+"'>"+url+"</a>"
    maintype= response.headers['Content-Type'].split(';')[0].lower()
    if maintype not in ('image/png', 'image/jpeg', 'image/gif'):
        return "<a href='"+url+"'>"+url+"</a>"
    else:
        return "<img src='"+url+"' width='500' height='250'></img>"


class showCompleteBlog(webapp2.RequestHandler):

    def get(self):
       JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                               extensions=['jinja2.ext.autoescape'],
                                               autoescape=False)
       template = JINJA_ENVIRONMENT.get_template('showCompleteBlog.html') 
       
       cur_url = self.request.url
       parsed_url = urlparse.urlparse(cur_url)
       blogid = urlparse.parse_qs(parsed_url.query)['blogid']
#       session = urlparse.parse_qs(parsed_url.query)['sessionId']
#       sessionId = int(session[0])
       
       login = 0
       user = ""
       username = ""
#       self.response.write(sessionId)
       user = users.get_current_user()
       
       if user:
           username = user.nickname()
           login = 1
       else:
           login = 0  

#       try:
#            user = UserLoggedIn.get_by_id(int(sessionId))
#            username = user.blogger.nickname()
#            login = 1
#       except db.BadKeyError:
#            login = 0
#       except NameError:
#            login = 0 
#       self.response.write(login) 
           
       b = Blogs.get_by_id(int(blogid[0]))
       
       query = "SELECT * FROM Comments WHERE blogid='"+blogid[0]+"'"
       comments_list = db.GqlQuery(query)
       count_comments = 0
       for c in comments_list:
           count_comments = count_comments + 1
       
  #     self.response.write(b.content)
       unicode_content = unicode(b.content, "utf8") 
       link_content = re.sub(r'(https?://[^\s]+)',convert,unicode_content)
   #    self.response.write(link_content)
       
       permalink = cur_url
       
       template_values = {'comments':comments_list,
                          'b': b,
                          'comment_count':count_comments,
                          'login' : login,
                          'cur_url' : cur_url,
                          'username' : username,
#                          'sessionId' : sessionId,
                          'content' : link_content,
                          'permalink' : permalink
                          }
       
       self.response.write(template.render(template_values))
       
application = webapp2.WSGIApplication([
    ('/showCompleteBlog.*', showCompleteBlog)
    ], debug=True)

