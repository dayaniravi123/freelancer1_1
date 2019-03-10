from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render_to_response, render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from employer.models import freelancer,project,employers,bid,freelancerTeam
from freelancer1_1 import settings


def signup(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login/signup1.html', c)

def handle_uploaded_photo(f):
    with open('Home/static/upload/p_photo/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def handle_uploaded_certificate(f):
    with open('Home/static/upload/certificate/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def addUser(request):
    uname = request.POST.get('uname')
    email = request.POST.get('email')
    password1 = request.POST.get('pass1')
    mobile=request.POST.get('mobile')
    user = User.objects.create_user(username=uname, email=email, password=password1)
    fre=freelancer(freelancerName=uname,skills="none",description="none",experience=0,education="none",qualifications="none",profilePhoto="none", password=password1,emailId=email,mobileNumber=mobile,address="none",certificates="none",bids=8)
    fre.save()
    user.save()
    #id=freelancer.objects.get(EmployerName=uname)
    return HttpResponseRedirect('/freelancer/registered/')


def registered(request):
    return render_to_response('login/addFreelancer.html')



def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    #user1=freelancer.objects.get(freelancerName=username)
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        request.session['fname'] = username
        auth.login(request, user)
        return HttpResponseRedirect('/freelancer/loggedin/')
    else:
        return HttpResponseRedirect('/freelancer/invalidlogin/')


@login_required(login_url='/freelancer/login/')
def loggedin(request):
    c1 = {}
    c1.update(csrf(request))
    fre = freelancer.objects.get(freelancerName=request.session['fname']).id
    freTeam=freelancerTeam.objects.filter(freelancer_id=fre)
    return render_to_response('login/loggedin.html', {"full_name": request.user.username,"freTeam":freTeam}, c1)


#@login_required(login_url='/loginmodule/freelancer/')
def invalidlogin(request):
    return render_to_response('login/invalidlogin.html')


def logout(request):
    auth.logout(request)
    return render_to_response('login/logout.html')

@login_required(login_url='/freelancer/login/')
def updateProfile(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login/updateprofile.html',c)

@login_required(login_url='/freelancer/login/')
def profileUpdation(request):
    f=freelancer.objects.get(freelancerName=request.session['fname'])
    f.freelancerName = request.POST.get('uname')
    f.skills = request.POST.get('skills')
    f.description = request.POST.get('description')
    if (request.method == 'POST'):
        fre = freelancer(request.POST, request.FILES)
        if fre is not None:
            handle_uploaded_photo(request.FILES['photo'])
            f.profilePhoto= request.FILES['photo'].name
        else:
            f.profilePhoto = "null"

    f.experience = request.POST.get('exper')
    # education=request.POST.get('education')
    f.qualifications = request.POST.get('qualification')
    f.education = request.POST.get('education')
    f.emailId = request.POST.get('email')
    f.password = request.POST.get('pass1')
    f.mobileNumber = request.POST.get('mobile')
    f.address = request.POST.get('address')
    if (request.method == 'POST'):
        fre = freelancer(request.POST, request.FILES)
        if fre is not None:
            handle_uploaded_certificate(request.FILES['file'])
            f.certificate = request.FILES['file'].name
        else:
            f.certificate = "null"

    # certificate=request.POST.get('certificate')
    user = User.objects.get(username=request.session['fname'])
    user.delete()
    user1 = User.objects.create_user(username=f.freelancerName, email=f.emailId, password=f.password)
    f.paytmLink=request.POST.get('paytm')
    f.save()
    user1.save()
    return render_to_response('login/loggedin.html')

@login_required(login_url='/freelancer/login/')
def placeBid(request,id):
    c={}
    c.update(csrf(request))
    pro=[]
    pro.append(project.objects.get(id=id))
    request.session['proj']=id
    return render(request,'login/placeBid.html',{"pro":pro},c)


@login_required(login_url='/freelancer/login/')
def addBid(request):
    pro=project.objects.get(id=request.session['proj'])
    fre=freelancer.objects.get(freelancerName=request.session['fname'])
    fre.bids-=1
    bidN=int(pro.bidNumber)+1
    pro.bidNumber=bidN
    proposal=request.POST.get('proposal','')
    price=request.POST.get('price','')
    days=request.POST.get('days','')
    team=request.POST.get('member','')
    b=bid(proposal=proposal,price=price,days=days,freelancerName_id=fre.id,proId_id=pro.id,team=team)
    b.save()
    pro.save()
    fre.save()
    return HttpResponseRedirect('/Home/display')

def updateTeam(request,id):
    c = {}
    c.update(csrf(request))
    fre = freelancerTeam.objects.get(id=id)
    request.session['tfid']=fre.id
    return render(request,'login/updateTeam.html',{"fre":fre},c)

def teamUpdation(request):
    id=request.session['tfid']
    fre=freelancerTeam.objects.get(id=id)
    fre.memberName=request.POST.get('mName')
    fre.experience=request.POST.get('mExpr')
    fre.mobileNo=request.POST.get('mMobile')
    fre.save()
    return HttpResponseRedirect('/freelancer/loggedin/')

def sendEmail(request):
    subject = "Thank You for Submiting Feedback"
    message = "\n\nThank you for contacting us. we will reply to your query soon.\n\n-Exam Hub.\n"
    #from_email = settings.EMAIL_HOST_USER
    to_list = ['devanshugohil1998@gmail.com']
    send_mail(subject, message, 'freelancerdjango@gmail.com', to_list)
    return render_to_response('login/loggedin.html')

def handle_uploaded_project(f,id):
    pro = project.objects.get(id=id).projectName
    f.name=pro+".zip"
    with open('Home/static/upload/project/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url='/freelancer/login/')
def uploadProject(request):
    c2 = {}
    c2.update(csrf(request))
    return render(request,'login/uploadProject.html',c2)

def projectUpdation(request):
    f = freelancer.objects.get(freelancerName=request.session['fname'])
    name=request.POST.get('pName','')
    pro=project.objects.get(projectName=name)
    if (request.method == 'POST'):
        fre = freelancer(request.POST, request.FILES)
        if fre is not None:
            handle_uploaded_project(request.FILES['file'],pro.id)
            pro.status='complete'
            pro.save()
            #f.certificate = request.FILES['file'].name
    return render_to_response('login/loggedin.html')