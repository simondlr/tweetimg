# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from boto.s3.connection import S3Connection

import json
from twython import Twython

#from django.conf.settings import TWITTER_KEY,TWITTER_SECRET,TWITTER_CALLBACK
from django.conf import settings
from django.template import RequestContext

def index(request):
    
    if 'oauth_verifier' in request.GET:
        #coming back from Twitter.
        oauth_verifier = request.GET['oauth_verifier']
        t_api = Twython(settings.TWITTER_KEY,settings.TWITTER_SECRET,request.session['OAUTH_TOKEN'],request.session['OAUTH_TOKEN_SECRET'])
        final_tokens = t_api.get_authorized_tokens(oauth_verifier)
        request.session['OAUTH_TOKEN'] = final_tokens['oauth_token']
        request.session['OAUTH_TOKEN_SECRET'] = final_tokens['oauth_token_secret']
        return HttpResponseRedirect("/post")
    else:
        t_api = Twython(settings.TWITTER_KEY,settings.TWITTER_SECRET)
        auth_props = t_api.get_authentication_tokens(callback_url=settings.TWITTER_CALLBACK)
        a_url = auth_props['auth_url']
        request.session['OAUTH_TOKEN'] = auth_props['oauth_token']
        request.session['OAUTH_TOKEN_SECRET'] = auth_props['oauth_token_secret']
    return render(request,'index.html',locals(),context_instance=RequestContext(request))

def post(request):
    
    if 'text' in request.POST:
        #process form, create image and post to Twitter.
        print request.POST['text']
        
        import PIL
        from PIL import ImageFont
        from PIL import Image
        from PIL import ImageDraw
        import textwrap
        import os
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        #font = ImageFont.truetype("http://fonts.googleapis.com/css?family=Open+Sans",25)
        font = ImageFont.truetype("%s/static/OpenSans.ttf" % (SITE_ROOT),12)
        img=Image.new("RGBA", (340,214),(255,255,255))
        draw = ImageDraw.Draw(img)
        
        margin = offset = 20
        for line in textwrap.wrap(request.POST['text'],50):
            draw.text((margin, offset),line,(0,0,0),font=font)
            offset += font.getsize(line)[1]
        img.save("temp.png")
        return render(request,'post.html',locals())
    elif 'OAUTH_TOKEN' in request.session:
        #display form
        return render(request,'post.html',locals())
    else:
        HttpResponseRedirect('/')

def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')

