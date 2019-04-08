
from django.urls import path
from django.views.generic import TemplateView

from freelancer.views import login, auth_view, logout, loggedin, invalidlogin, updateProfile, signup, addUser, \
    registered, addBid, placeBid, sendEmail, profileUpdation, uploadProject, projectUpdation, updateTeam, teamUpdation, \
    chatInit, chatBeginning, viewprofile, varified, membership, premierMembership, professionalMembership, \
    basicMembership, chat, getMoney, withdraw, withdrawSuccess, addTeam, memberAdd, chatReq, cancelChat
from django.contrib.auth import views as auth_views
from django.conf.urls import url
urlpatterns = [
    url(r'^login/$', login),
    url(r'^auth/$', auth_view),
    url(r'^logout/$', logout),
    url(r'^loggedin/$', loggedin),
    url(r'^invalidlogin/$', invalidlogin),
    path('updateProfile/', updateProfile),
    path('profileUpdation/', profileUpdation),
    url(r'^signup/$', signup),
    url(r'^registered/$', registered),
    url(r'^addUser/$', addUser),
    url(r'^membership/$', membership),
    url(r'^premierMembership/$', premierMembership),
    url(r'^professionalMembership/$', professionalMembership),
    url(r'^basicMembership/$', basicMembership),
    url(r'^addBid/$',addBid),
    url(r'^memberAdd/$', memberAdd),
    url(r'^addTeam/$', addTeam),

    url(r'^updateTeam/(\d+)/$',updateTeam),
    url(r'^teamUpdation/$',teamUpdation),
    path('uploadProject/',uploadProject),
    path('viewprofile/',viewprofile),
    path('projectUpdation/', projectUpdation),
    url(r'^sendEmail/$', sendEmail),
    url(r'^chatInit/$',chatInit),
    url(r'^cancelChat/$', cancelChat),
    url(r'^chatReq/$',chatReq),
    url(r'^chat/$',chat),
    url(r'^chatBeginning/(\d+)/$',chatBeginning),
    url(r'^varified/$',varified),
    url(r'^placeBid/(\d+)/$',placeBid),
    url(r'^withdraw/$', withdraw),
    url(r'^withdrawSuccess/$', withdrawSuccess),
    url(r'^getMoney/$', getMoney),

    #url(r'^signup/$', TemplateView.as_view(template_name='loginmodule/signup.html',content_type='text/html')),
    #path('transfer/', transfer),
]