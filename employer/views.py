import datetime
import io
import json
import random
import zipfile
from datetime import timedelta

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from firebase import firebase

from employer.models import employers, project, chat, freelancer
from django.contrib import auth
# Create your views here.
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from employer.models import employers,project,bid


def signup(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('employer/signup.html', c)


def addUser(request):
    uname = request.POST.get('uname')
    email = request.POST.get('email')
    password1 = request.POST.get('pass1')
    mobile=request.POST.get('mobile')
    Emp=employers(EmployerName=uname, Password=password1,MobileNumber=mobile,EmailId=email)
    user = User.objects.create_user(username=uname, email=email, password=password1)
    request.session["email"]=email
    Emp.save()
    user.save()
    id=employers.objects.get(EmployerName=uname)
    return HttpResponseRedirect('/employer/registered/')


def registered(request):
    c={}
    c.update(csrf(request))
    otp=random.randint(0,100000)
    subject = "Please Don't Share OTP"
    message = "\n\nYour OTP is "+str(otp)+".\n\n-Exam Hub.\n"
    # from_email = settings.EMAIL_HOST_USER
    request.session["otp"]=str(otp)
    to_list = [request.session["email"]]
    send_mail(subject, message, 'freelancerdjango@gmail.com', to_list)
    return render_to_response('employer/addEmployer.html',c)

def varified(request):
    tOtp=request.POST.get('otp','')
    sOtp=request.session["otp"]
    if tOtp==sOtp:
        return HttpResponseRedirect('/employer/login/')
    return render_to_response('employer/error.html')

def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('employer/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user=auth.authenticate(username=username, password=password)
    if user is not None:
        request.session['ename'] = username
        auth.login(request, user)
        return HttpResponseRedirect('/employer/loggedin/')
    else:
        return HttpResponseRedirect('/employer/invalidlogin/')


@login_required(login_url='/employer/login/')
def loggedin(request):
    emp=employers.objects.get(EmployerName=request.session['ename'])
    p=[]
    p=project.objects.filter(EmpId_id=emp.id)
    c1 = {}
    c1.update(csrf(request))
    return render_to_response('employer/loggedin.html', {"full_name": request.session['ename'],"projectList":p}, c1)


#@login_required(login_url='/loginmodule/freelancer/')
def invalidlogin(request):
    return render_to_response('employer/invalidlogin.html')


def logout(request):
    auth.logout(request)
    return render_to_response('employer/logout.html')

@login_required(login_url='/employer/login/')
def projectSubmit(request):
    c={}
    c.update(csrf(request))
    return  render_to_response('employer/projectSubmission.html',c)

def handle_uploaded_file(f):
    with open('Home/static/upload/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required(login_url='/employer/login/')
def projectSubmission(request):
    projectName = request.POST.get('pname', '')
    description = request.POST.get('description', '')

    skills = request.POST.get('skills', '')
    typeOfProject = request.POST.get('typeOfProject', '')
    price = request.POST.get('price', '')
    payType = request.POST.get('payType', '')
    # email=request.POST.get('email','')
    if (request.method == 'POST'):
        emp = employers(request.POST, request.FILES)
        if emp is not None:
            handle_uploaded_file(request.FILES['file'])
            file = request.FILES['file'].name
        else:
            file = "null"
    empy = employers.objects.get(EmployerName=request.session['ename']).id
    sDate = datetime.now()
    eDate = sDate + timedelta(days=7)
    # eDate=datetime.strptime(eDate,'%Y-%m-%d')
    m = sDate.month
    y = sDate.year
    d = sDate.day
    sDate = datetime(y, m, d)
    sDate = sDate.strftime('%Y-%m-%d')
    m = eDate.month
    y = eDate.year
    d = eDate.day
    eDate = datetime(y, m, d)
    eDate = eDate.strftime('%Y-%m-%d')
    # eDate=datetime.datetime(y,m,changedDate)
    bidN = 0
    p = project(projectName=projectName, description=description, files=file, skills=skills,typeOfProject=typeOfProject, price=price, payType=payType, bidNumber=bidN, startDate=sDate,endDate=eDate, EmpId_id=empy)
    p.save()
    return render_to_response('employer/success.html',{"succ":"Project is successfully posted."})


def satisfy(request,id):
    emp = employers.objects.get(EmployerName=request.session['ename'])
    p = []
    p = project.objects.filter(EmpId_id=emp.id)
    pro=project.objects.get(id=id)
    pro.status="payment"
    pro.save()
    c1 = {}
    c1.update(csrf(request))
    return render_to_response('employer/satisfy.html', {"full_name": request.session['ename'], "projectList": p}, c1)


def downloadProject(request,name):
    filename = 'Home/static/upload/project/'+name+".zip"
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as backup_zip:
        backup_zip.write(filename)  # u can also make use of list of filename location
        # and do some iteration over it
    response = HttpResponse(zip_io.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = zip_io.tell()
    return response

def chat(request):
    c={}
    c.update(csrf(request))
    f = firebase.FirebaseApplication('https://freelancer1-73000.firebaseio.com', None)
    name = '/User/' + request.session['ename'] + '/'
    result = f.get(name, '')
    if result is None:
        result={
        'receiver': "",
        'receiverMsg': "",
        'sendMsg':""
        }
    #print(str(result))
    #print(str(result['receiveMsg']))
    req=str(result['request'])
    send=str(result['sendMsg'])
    rec=str(result['receiveMsg'])
    recv=str(result['receiver'])
    print(req)
    ans="n"
    return render(request,'employer/chatBegin.html',{"recv":recv,"ans":ans,"req":req,"send": send, "rec": rec},c)

def chatReq(request):
    c={}
    c.update(csrf(request))
    f = firebase.FirebaseApplication('https://freelancer1-73000.firebaseio.com', None)
    name = '/User/' + request.session['ename'] + '/'
    result = f.get(name, '')
    recv = str(result['receiver'])
    f.put(name,"request","done")
    name1 = '/User/' + recv + '/'
    re=f.get(name1,'')
    f.put(name1,"request","done")
    f.put(name1, "Accept", "Yes")
    send = str(result['sendMsg'])
    rec = str(result['receiveMsg'])
    recv=str(result['receiver'])
    accept=str(result['Accept'])
    ack="Yes"
    return render(request,'employer/chat.html',{"act":accept,"ack":ack,"recv":recv,"send": send, "rec": rec},c)

def chatInit(request):
    c={}
    c.update(csrf(request))
    f = firebase.FirebaseApplication('https://freelancer1-73000.firebaseio.com', None)
    tName = '/User/' + request.session['ename'] + '/'
    result = f.get(tName, '')
    ch=str(result['receiver'])
    name = '/User/' + ch + '/'
    result=f.get(name ,'')
    rec = str(result['sendMsg'])
    send=request.POST.get('send','')

    tName='/User/'+request.session['ename']+'/'
    result = f.put(tName,"receiveMsg", str(rec))
    result = f.put(tName,"sendMsg",str(send))
    #print("result")
    #print("result is"+str(result['name']))
    #request.session['skey']=str(result['name'])
    #for receiver
    tName = '/User/' + ch + '/'
    data = {
        'receiver': request.session['ename'],
        'receiverMsg': send,
        'sendMsg':""
    }
    result1 = f.put(tName, "receiver",request.session['ename'])
    result1=f.put(tName,"receiveMsg",str(send))
    name = '/User/' + request.session['ename'] + '/'
    result = f.get(name, '')
    #print(str(result))
    #print(str(result['receiveMsg']))
    send = str(result['sendMsg'])
    rec = str(result['receiveMsg'])
    if str(result['request'])=="n":
        return HttpResponseRedirect('/employer/chat/')
    return render(request, 'employer/chat.html', {"send": send, "rec": rec},c)

def cancelChat(request):
    f = firebase.FirebaseApplication('https://freelancer1-73000.firebaseio.com', None)
    tName = '/User/' + request.session['ename'] + '/'
    result = f.get(tName, '')
    ch = str(result['receiver'])
    rs=f.put(tName,"request","n")
    rs=f.put(tName,"Accept","No")
    tName = '/User/' + ch + '/'
    result = f.get(tName, '')
    rs=f.put(tName,"request","n")
    rs=f.put(tName,"Accept","No")
    return HttpResponseRedirect("/employer/loggedin/")

def getMoney(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'employer/getMoney.html', c)

def withdraw(request):
    c = {}
    c.update(csrf(request))
    name=request.POST.get('name','')
    number = request.POST.get('number', '')
    amount=request.POST.get('amount','')
    request.session['amount']=int(amount)
    otp = random.randint(0, 10000)
    # f=freelancer.objects.get(freelancerName=request.session['tfname'])
    e = employers.objects.get(EmployerName=request.session['ename'])
    if int(e.Money) < int(amount):
        return render_to_response('employer/failure.html')
    subject = "Please Don't Share OTP"
    message = "\n\nYour OTP is " + str(otp) + ".\n\n-Employment Hub.\n"
    # from_email = settings.EMAIL_HOST_USER
    request.session["emaotp"] = str(otp)
    to_list = [e.EmailId]
    send_mail(subject, message, 'freelancerdjango@gmail.com', to_list)
    return render_to_response('employer/withdrawVarified.html', c)

def withdrawSuccess(request):
    otp = request.POST.get('otp', '')
    votp = request.session['emaotp']
    if otp == votp:
        e = employers.objects.get(EmployerName=request.session['ename'])
        Money = e.Money -int(request.session['amount'])
        e.Money = Money
        e.save()
        return render_to_response('employer/success.html',{"succ":"withdraw money successfully"})
    else:
        return render_to_response('employer/failure.html')



def addMoney(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'employer/addMoney.html', c)

def deposite(request):
    c = {}
    c.update(csrf(request))
    name = request.POST.get('name', '')
    number = request.POST.get('number', '')
    amount=request.POST.get('amount','')
    request.session['amount']=int(amount)
    date = request.POST.get('date', '')
    csv = request.POST.get('csv', '')
    otp = random.randint(0, 10000)
    # f=freelancer.objects.get(freelancerName=request.session['tfname'])
    e = employers.objects.get(EmployerName=request.session['ename'])
    subject = "Please Don't Share OTP"
    message = "\n\nYour OTP is " + str(otp) + ".\n\n-Employment Hub.\n"
    # from_email = settings.EMAIL_HOST_USER
    request.session["emaotp"] = str(otp)
    to_list = [e.EmailId]
    send_mail(subject, message, 'freelancerdjango@gmail.com', to_list)
    return render_to_response('employer/depositeVarified.html', c)

def depositSuccess(request):
    otp = request.POST.get('otp', '')
    votp = request.session['emaotp']
    if otp == votp:
        e = employers.objects.get(EmployerName=request.session['ename'])
        Money = e.Money +int(request.session['amount'])
        e.Money = Money
        e.save()
        return render_to_response('employer/success.html',{"succ":"deposit money successfully"})
    else:
        return render_to_response('employer/failure.html')

def payment(request,id):
    c={}
    c.update(csrf(request))
    f=project.objects.get(id=id)
    request.session['pid']=id
    request.session['tfname']=f.finalSelection
    return render(request,'employer/payment.html',{"fre":f.finalSelection},c)

def paymentProcess(request):
    c={}
    c.update(csrf(request))
    name=request.POST.get('name','')
    number=request.POST.get('number','')
    date=request.POST.get('date','')
    csv=request.POST.get('csv','')
    otp=random.randint(0,10000)
    #f=freelancer.objects.get(freelancerName=request.session['tfname'])
    e=employers.objects.get(EmployerName=request.session['ename'])
    subject = "Please Don't Share OTP"
    message = "\n\nYour OTP is " + str(otp) + ".\n\n-Employment Hub.\n"
    # from_email = settings.EMAIL_HOST_USER
    request.session["potp"] = str(otp)
    to_list = [e.EmailId]
    send_mail(subject, message, 'freelancerdjango@gmail.com', to_list)
    return render_to_response('employer/varifiedOtp.html',c)

def varified(request):
    otp=request.POST.get('otp','')
    votp=request.session['potp']
    if otp==votp:
        f=freelancer.objects.get(freelancerName=request.session['tfname'])
        p=project.objects.get(id=request.session['pid'])
        Money=f.Money+p.price
        f.Money=Money
        f.save()
        e=employers.objects.get(EmployerName=request.session['ename'])
        Money=e.Money-p.price
        e.Money=Money
        e.save()
        return render_to_response('employer/success.html',{"succ":"payment done successfully"})
    else:
        return render_to_response('employer/failure.html')