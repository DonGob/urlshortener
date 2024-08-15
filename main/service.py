import random
import string
import re
from .models import LinkMapping
from django.http import HttpResponse
from django.shortcuts import redirect

def get_random_shortcode():
    random_shortcode = ''.join(random.choice(string.ascii_letters + string.digits + '_') for _ in range(6))\
    
    #check if shortcode does not yet exist in database
    if not LinkMapping.objects.shortcode_exists(random_shortcode):
        return random_shortcode
    else:
        while LinkMapping.objects.shortcode_exists(random_shortcode): #keep generating new code until we get a unique one
            random_shortcode = ''.join(random.choice(string.ascii_letters + string.digits + '_') for _ in range(6))
        return random_shortcode

def redirect_shortcode(shortcode):
    shortcode_object = LinkMapping.objects.get(shortcode=shortcode)
    url = shortcode_object.originalUrl
    shortcode_object.update_last_redirect_and_count()
    return redirect(url)

def test_url(url):
    if not url:
        return HttpResponse("<h1>400 Url not present</h1>", status=400)
    else:
        return
    
def test_shortcode(shortcode, url):
    if LinkMapping.objects.shortcode_exists(shortcode):
        if url == LinkMapping.objects.get(shortcode=shortcode).originalUrl:
            return HttpResponse("<h1>409 Shortcode already linked to the supplied url </h1>", status=409)
        return HttpResponse("<h1>409 Shortcode already in use </h1>", status=409)
    elif not bool(re.match('^[\w]{6}$', shortcode)):
        return HttpResponse("<h1>412 The provided shortcode is invalid</h1>", status=412)
    else:
        return