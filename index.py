# -*- coding:utf-8 -*- ＃必须在第一行或者第二行
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import urlfetch
import urllib
import base64

import os
from google.appengine.ext.webapp import template
#\lib\django\django\template

from zd_db import *


class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      header(self,"Twitter更新")
      template_values = {
            'nickname': user.nickname(),
      }

      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))

      footer(self)

    else:
      self.redirect(users.create_login_url(self.request.uri))

class UpdateTWT(webapp.RequestHandler):
  def post(self):
    sys_err = 0
    err_msg = ""
    update_url = 'http://twitter.com/statuses/update.xml'
    form = cgi.FieldStorage()
    if not (form.has_key("id") and form.has_key("passwd") and form.has_key("content")):
      err_msg = "请填写以下内容 UserID, Password and Messages.<br>"
      sys_err=1
    else:
      if len(form["id"].value) < 3 or len(form["id"].value) > 20:
        err_msg += "UserID必须是3-20个字符.<br>"
        sys_err=1
      
      if len(form["passwd"].value) < 6 or len(form["passwd"].value) > 50:
        err_msg += "Password必须是6-50个字符.<br>"
        sys_err=1
      
      if len(form["content"].value) < 3 or len(form["content"].value) > 130:
        err_msg += "Messages必须是3-130个字符.<br>"
        sys_err=1


    if sys_err == 0:

      username = cgi.escape(self.request.get('id'))
      password = cgi.escape(self.request.get('passwd'))
      form_fields = {
        "status": cgi.escape(self.request.get('content'))
      }
      form_data = urllib.urlencode(form_fields)
      base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
      result = urlfetch.fetch(url=update_url,
                            payload=form_data,
                            method=urlfetch.POST,
                            headers={
                              'Content-Type': 'application/x-www-form-urlencoded',
                              'Authorization': 'Basic '+ base64string
                            })

      header(self,"Twitter更新")

      if result.status_code == 200:
        self.response.out.write('Twitter更新成功:<pre>')
        self.response.out.write(cgi.escape(self.request.get('content')))
        self.response.out.write('</pre>')
      else:
        self.response.out.write('Twitter更新失败['+cgi.escape(result.status_code)+']:<pre>')
        self.response.out.write(cgi.escape(self.request.get('content')))
        self.response.out.write('</pre>')
    
      footer(self)
    
    else:
      header(self,"出错")
      self.response.out.write('<h1>Error</h1>')
      self.response.out.write('<font color=red>'+err_msg+'</font>')
      footer(self)

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/update', UpdateTWT)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()