"""

.. module:: views
   :synopsis: The views associated with compose.

.. moduleauthor:: Rob Madden <rob@sproutsocial.com>

"""

import datetime

from django.http import HttpResponse
from django.template import RequestContext, Context
from django.template.loader import get_template

from data import Data

def html(request):
    data = Data()
    t = get_template('index.html')
    c = RequestContext(request, {"date": datetime.datetime.now(), "teams": data.get_teams()})
    html = t.render(c)
    return HttpResponse(html)