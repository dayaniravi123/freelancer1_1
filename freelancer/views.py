import json
import random

#import firebase as firebase
from firebase import firebase
#from firebase.firebase import FirebaseApplication
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render_to_response, render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from employer.models import freelancer, project, employers, bid, freelancerTeam, chat
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
    request.session["email"]=email
    fre.save()
    user.save()
    #id=freelancer.objects.get(EmployerName=uname)
    return HttpResponseRedirect('/freelancer/registered/')


def registered(request):
    c={}
    c.update(csrf(request))
    otp=random.randint(0,100000)
    subject = "Please Don't Share OTP"
    message = "\n\nYour OTP is "+str(otp)+".\n\n-Employment Hub.\n"
    # from_email = settings.EMAIL_HOST_USER
    request.session["otp"]=str(otp)
    to_list = [request.session["email"]]
    send_mail(subject, message, 'freelancerdjango@gmail.com', to_list)
    return render_to_response('login/addFreelancer.html',c)

def varified(request):
    tOtp=request.POST.get('otp','')
    sOtp=request.session["otp"]
    if tOtp==sOtp:
        return HttpResponseRedirect('/freelancer/login/')
    return render_to_response('employer/error.html')

def membership(request):
    return render_to_response('login/bidPlans.html')

def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    #user1=freelancer.objects.get(freelancerName=username)
    user = auth.authenticate(username=username, password=password)
    if username=="root" and password=="root1234":
        auth.login(request,user)
        return HttpResponseRedirect('/admin/showHome/')
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
    fre = freelancer.objects.get(freelancerName=request.session['fname'])
    freTeam=freelancerTeam.objects.filter(freelancer_id=fre.id)
    p = bid.objects.filter(freelancerName_id=fre.id)
    a=[]
    for i in p:
        a.append(project.objects.get(id=i.proId_id))

    return render_to_response('login/loggedin.html', {"full_name": request.user.username,"a":a,"freTeam":freTeam}, c1)

def viewprofile(request):
    fre= freelancer.objects.get(freelancerName=request.session['fname'])
    return render_to_response('login/profile.html',{"fre":fre})



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
    fBid = freelancer.objects.get(freelancerName=request.session['fname']).bids
    #print(str(fBid))
    if fBid <= 0:
        return render_to_response('login/bidPlans.html')

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
    return HttpResponseRedirect('/freelancer/loggedin/')

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

def premierMembership(request):
    f=freelancer.objects.get(freelancerName=request.session['fname'])
    bids=int(f.bids)+100
    f.bids=bids
    f.save()
    return HttpResponseRedirect('/freelancer/viewprofile/')

def professionalMembership(request):
    f=freelancer.objects.get(freelancerName=request.session['fname'])
    bids=int(f.bids)+45
    f.bids=bids
    f.save()
    return HttpResponseRedirect('/freelancer/viewprofile/')

def basicMembership(request):
    f=freelancer.objects.get(freelancerName=request.session['fname'])
    bids=int(f.bids)+10
    f.bids=bids
    f.save()
    return HttpResponseRedirect('/freelancer/viewprofile/')

def chat(request):
    c = {}
    c.update(csrf(request))
    #request.session['fname'] = 'devan'
    f = firebase.FirebaseApplication('https://freelancer1-73000.firebaseio.com', None)
    name = '/User/' + request.session['fname'] + '/'
    #name = '/User/' + request.session['fname'] + '/'+request.session['rkey']+'/'
    result = f.get(name, '')
    if result is None:
        result = {
            'receiver': "",
            'receiverMsg': "",
            'sendMsg': ""
        }
    #print(str(result))
    #print(str(result['receiveMsg']))
    send = str(result['sendMsg'])
    rec = str(result['receiveMsg'])
    return render(request, 'login/chat.html', {"send": send, "rec": rec}, c)


def chatInit(request):
    ch = request.POST.get('username', '')

    #send mail for chatting
    subject ="Please Open chat Window"
    message = "\n\n"+ch+" want to chat with you.\nPlease give reply. "+"-Employment Hub.\n"
    frelanc=employers.objects.get(EmployerName=ch)
    to_list = [frelanc.EmailId]
    send_mail(subject, message, 'freelancerdjango@gmail.com', to_list)

    #send message
    f = firebase.FirebaseApplication('https://freelancer1-73000.firebaseio.com', None)
    #name = '/User/' + ch + '/'
    name = '/User/' + ch + '/'+request.session['skey']+'/'
    result = f.get(name, '')
    rec = str(result['sendMsg'])

    send = request.POST.get('send', '')
    data = {
        'receiver': ch,
        'receiverMsg': rec,
        'sendMsg': send
    }
    tName = '/User/' + request.session['fname'] + '/'
    result = f.post(tName, data)
    print(result)
    request.session['rkey']=str(result['name'])
    tName = '/User/' + ch + '/'
    data = {
        'receiver': request.session['fname'],
        'receiverMsg': send,
        'sendMsg': ""
    }
    result1 = f.post(tName, data)
    request.session['rkey1'] = str(result1['name'])
    name = '/User/' + request.session['fname'] + '/'
    result = f.get(name, '')
    return render(request, 'login/chat.html', {"send": send, "rec": rec})

def getMoney(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'login/getMoney.html', c)

def withdraw(request):
    c = {}
    c.update(csrf(request))
    name=request.POST.get('name','')
    number = request.POST.get('number', '')
    amount=request.POST.get('amount','')
    request.session['amount']=int(amount)
    otp = random.randint(0, 10000)
    # f=freelancer.objects.get(freelancerName=request.session['tfname'])
    f = freelancer.objects.get(freelancerName=request.session['fname'])
    if int(f.Money) < int(amount):
        return render_to_response('freelancer/failure.html')
    subject = "Please Don't Share OTP"
    message = "\n\nYour OTP is " + str(otp) + ".\n\n-Employment Hub.\n"
    # from_email = settings.EMAIL_HOST_USER
    request.session["emaotp"] = str(otp)
    to_list = [f.emailId]
    send_mail(subject, message, 'freelancerdjango@gmail.com', to_list)
    return render_to_response('login/withdrawVarified.html', c)

def withdrawSuccess(request):
    otp = request.POST.get('otp', '')
    votp = request.session['emaotp']
    if otp == votp:
        f = freelancer.objects.get(freelancerName=request.session['fname'])
        Money = f.Money -int(request.session['amount'])
        f.Money = Money
        f.save()
        return render_to_response('login/success.html')
    else:
        return render_to_response('login/failuer.html')


def chatBeginning(request,id):
    c=chat.objects.get(id=id)
    c.messageRes=request.POST.get('msgr','')
    #ch=chat(messageRes=msg)
    c.save()
    return render_to_response('/loggedin.html')