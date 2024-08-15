from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shorten', views.process_shorten_request, name='shorten_post'),
    path('get', views.handle_shortcode_request, name='handle_shortcode_request'),
    path('<str:shortcode>', views.redirect_from_url, name='redirect_from_url'),
]