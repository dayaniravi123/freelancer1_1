from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^show/$',views.show),
    url(r'^showProj/$',views.showProj),
    url(r'^search/$', views.search),
    url(r'^showBid/(\d+)/$',views.showBid),
    url(r'selectFreelancer/(\d+)/$',views.selectFreelancer),

]