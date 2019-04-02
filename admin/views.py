# Create your views here.
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from employer.models import freelancer, employers


def showHome(request):
    return render_to_response('admin/home.html')


def logout(request):
    auth.logout(request)
    return render_to_response('login/logout.html')

#for freelancer

def showFreelancer(request):
    f=freelancer.objects.all()
    return render_to_response('admin/showFreelancer.html',{"f":f})

def showDetail(request,id):
    fre=freelancer.objects.get(id=id)
    return render_to_response('admin/showDetail.html',{"fre":fre})

def block(request, id):
    fre=freelancer.objects.get(id=id)
    u=User.objects.get(username=fre.freelancerName)
    fre.delete()
    u.delete()
    return HttpResponseRedirect('/admin/showFreelancer/')

#for employer

def showEmployer(request):
    f=employers.objects.all()
    return render_to_response('admin/showEmployer.html',{"f":f})

def showDetailEmp(request,id):
    emp=employers.objects.get(id=id)
    return render_to_response('admin/showDetailEmp.html',{"emp":emp})

def blockEmp(request,id):
    emp=employers.objects.get(id=id)
    u = User.objects.get(username=emp.EmployerName)
    u.delete()
    emp.delete()
    return HttpResponseRedirect('/admin/showEmployer/')

