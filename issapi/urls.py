"""URL for issapi"""

from django.conf.urls import url

from issapi import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    
]
