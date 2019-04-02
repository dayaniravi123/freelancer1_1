from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.signup),
    url(r'^registered/$', views.registered),
    url(r'^varified/$',views.varified),
    url(r'^addUser/$', views.addUser),
    url(r'^login/$',views.login),
    url(r'^auth/$', views.auth_view),
    url(r'^logout/$', views.logout),
    url(r'^loggedin/$', views.loggedin),
    url(r'^invalidlogin/$', views.invalidlogin),
    url(r'^projectSubmit/$', views.projectSubmit),
    url(r'^projectSubmission/$',views.projectSubmission),
    url(r'^satisfy/$',views.satisfy),
    url(r'^downloadProject/([a-zA-Z ]*)/$',views.downloadProject),
    url(r'^chatInitiated/$',views.chatInitiated),
    url(r'^chatBeginning/$',views.chatBeginning),
]
