"""

.. module:: views
   :synopsis: The views associated with compose.

.. moduleauthor:: Rob Madden <rob@sproutsocial.com>

"""

import datetime

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

def html(request):
    t = get_template('index.html')
    c = Context({"date": datetime.datetime.now()})
    html = t.render(c)
    return HttpResponse(html)