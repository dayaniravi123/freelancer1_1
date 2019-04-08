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
    url(r'^satisfy/(\d+)/$',views.satisfy),
    url(r'^downloadProject/([a-zA-Z ]*)/$',views.downloadProject),
    url(r'^chat/$',views.chat),
    url(r'^chatReq/$', views.chatReq),
    url(r'^cancelChat/$', views.cancelChat),
    url(r'^chatInit/$',views.chatInit),
    url(r'^payment/(\d+)/$',views.payment),
    url(r'^paymentProcess/$',views.paymentProcess),
    url(r'^varified/$',views.varified),
    url(r'^deposite/$', views.deposite),
    url(r'^depositSuccess/$', views.depositSuccess),
    url(r'^addMoney/$', views.addMoney),
    url(r'^withdraw/$', views.withdraw),
    url(r'^withdrawSuccess/$', views.withdrawSuccess),
    url(r'^getMoney/$', views.getMoney),

]
