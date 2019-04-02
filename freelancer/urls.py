
from django.urls import path
from django.views.generic import TemplateView

from freelancer.views import login, auth_view, logout, loggedin, invalidlogin, updateProfile, signup, addUser, \
    registered, addBid, placeBid, sendEmail, profileUpdation, uploadProject, projectUpdation, updateTeam, teamUpdation, \
    chatInitiated, chatBeginning, viewprofile, varified, membership
from django.contrib.auth import views as auth_views
from django.conf.urls import url
urlpatterns = [
    url(r'^login/$', login),
    url(r'^auth/$', auth_view),
    url(r'^logout/$', logout),
    url(r'^loggedin/$', loggedin),
    url(r'^invalidlogin/$', invalidlogin),
    path('updateprofile/', updateProfile),
    path('profileUpdation/', profileUpdation),
    url(r'^signup/$', signup),
    url(r'^registered/$', registered),
    url(r'^addUser/$', addUser),
    url(r'^membership/$', membership),
    url(r'^addBid/$',addBid),
    url(r'^updateTeam/(\d+)/$',updateTeam),
    url(r'^teamUpdation/$',teamUpdation),
    path('uploadProject/',uploadProject),
    path('viewprofile/',viewprofile),
    path('projectUpdation/', projectUpdation),
    url(r'^sendEmail/$', sendEmail),
    url(r'^chatInitiated/$',chatInitiated),
    url(r'^chatBeginning/(\d+)/$',chatBeginning),
    url(r'^varified/$',varified),
    url(r'^placeBid/(\d+)/$',placeBid),
    #url(r'^signup/$', TemplateView.as_view(template_name='loginmodule/signup.html',content_type='text/html')),
    #path('transfer/', transfer),
]