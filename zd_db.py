#zd_db module

import os
from google.appengine.ext.webapp import template

def header(self,title=""):
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

    template_values = {
            'title': title,
    }
    path = os.path.join(os.path.dirname(__file__), 'header.html')
    self.response.out.write(template.render(path, template_values))


def footer(self):
    template_values = {

    }
    path = os.path.join(os.path.dirname(__file__), 'footer.html')
    self.response.out.write(template.render(path, template_values))

