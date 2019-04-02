import datetime
import io
import random
import zipfile

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from employer.models import employers, project, chat
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
    projectName=request.POST.get('pname','')
    description=request.POST.get('description','')

    skills=request.POST.get('skills','')
    typeOfProject=request.POST.get('typeOfProject','')
    price=request.POST.get('price','')
    payType=request.POST.get('payType','')
    #email=request.POST.get('email','')
    if(request.method=='POST'):
        emp=employers(request.POST,request.FILES)
        if emp is not None :
            handle_uploaded_file(request.FILES['file'])
            file=request.FILES['file'].name
        else:
            file="null"

    empy=employers.objects.get(EmployerName=request.session['ename']).id
    sDate=datetime.datetime.now()
    changedDate=int(sDate.day)+1
    m=sDate.month
    y=sDate.year
    eDate=datetime.datetime(y,m,changedDate)
    bidN=0
    sDate = datetime.strptime(sDate, '%Y-%m-%d')
    sDate = sDate.strftime('%Y-%m-%d')
    p=project(projectName=projectName,description=description,files=file,skills=skills,typeOfProject=typeOfProject,price=price,payType=payType,bidNumber=bidN,startDate=sDate,endDate=eDate,EmpId_id=empy)
    p.save()
    return render_to_response('employer/success.html')

def satisfy(request):
    emp = employers.objects.get(EmployerName=request.session['ename'])
    p = []
    p = project.objects.filter(EmpId_id=emp.id)
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


def chatInitiated(request):
    c={}
    c.update(csrf(request))
    return render_to_response('employer/chat.html',c)

def chatBeginning(request):
    msg=request.POST.get('msg','')
    ch=chat(messageReq=msg,messageRes="")
    ch.save()
    return render_to_response('employer/loggedin.html')