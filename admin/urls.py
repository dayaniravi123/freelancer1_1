from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^showHome/$', views.showHome),
    url(r'^showFreelancer/$',views.showFreelancer),
    url(r'^logout',views.logout),
    url(r'^showDetail/(\d+)/$',views.showDetail),
    url(r'^block/(\d+)/$',views.block),
    url(r'^showEmployer/$', views.showEmployer),
    url(r'^showDetailEmp/(\d+)/$', views.showDetailEmp),
    url(r'^blockEmp/(\d+)/$', views.blockEmp),

]
