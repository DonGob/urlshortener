from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from . import service
from .models import LinkMapping

def process_shorten_request(request):
    url = request.POST['url']
    shortcode = request.POST['shortcode']

    if not shortcode: #if no shortcode is provided
        shortcode = service.get_random_shortcode()

    url_test_response = service.test_url(url)
    if url_test_response: #if an error response was returned by test_url
        return url_test_response
    
    shortcode_test_response = service.test_shortcode(shortcode, url)
    if shortcode_test_response: #if an error response was returned by test_shortcode
        return shortcode_test_response

    LinkMapping.objects.create(originalUrl=url, shortcode=shortcode)
    shortened_url = request.build_absolute_uri(reverse('redirect_from_url', args=[shortcode]))
    return HttpResponse(f'shortcode: {shortcode} <br> Shortened URL: <a href="{shortened_url}">{shortened_url}</a>', status=201)

def index(request):
    return render(request, 'main/index.html')

def redirect_from_url(request, shortcode):
    return service.redirect_shortcode(shortcode)

def handle_shortcode_request(request):
    shortcode = request.GET['shortcode']
    if not LinkMapping.objects.shortcode_exists(shortcode):
        return HttpResponse(f'<h1> 404 Shortcode not found </h1>', status=404)

    if request.GET['request_type'] == 'redirect':
        return service.redirect_shortcode(shortcode)
    elif request.GET['request_type'] == 'stats':
        shortcode_object = LinkMapping.objects.get(shortcode=shortcode)
        return HttpResponse(f"created: {shortcode_object.created} <br> lastRedirect: {shortcode_object.lastRedirect} <br> redirectCount: {shortcode_object.redirectCount}")

        
