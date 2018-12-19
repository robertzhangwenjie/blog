from django.shortcuts import render
import logging
from django.conf import settings
logger = logging.getLogger('my_blog.views')

# Create your views here.
def global_settings(request):
    return {'SITE_NAME' : settings.SITE_NAME,
        'SITE_DESC' : settings.SITE_DESC,
        'WEIBO_SINA' : settings.WEIBO_SINA,
        'WEIBO_TECENT' : settings.WEIBO_TECENT,
        'PRO_RSS' : settings.PRO_RSS,
        'PRO_EMAIL' : settings.PRO_EMAIL
            }

def index(request):
    try:
        file = open('./test','r')
    except Exception as e:
        logger.error(e)
    return render(request,'index.html',locals())