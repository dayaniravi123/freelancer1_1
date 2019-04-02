from django.shortcuts import render, render_to_response
from employer.models import project, bid,freelancer
from django.template.context_processors import csrf
from datetime import datetime

def show(request):
    r={}
    r.update(csrf(request))
    c=[]
    c=project.objects.all()
    b=[]
    d=[]
    b=bid.objects.all()
    cDate = datetime.now()
    cDate = cDate.strftime('%Y-%m-%d')

    for pro in c:
        proDate = datetime.strptime(pro.endDate, '%Y-%m-%d')
        proDate = proDate.strftime('%Y-%m-%d')
        if proDate > cDate:
            d.append(pro)

    return render(request,'Project/project.html',{"c":d,"b":b},r)

def showProj(request):
    budget=request.POST.getlist('check')
    type=request.POST.getlist('check1')
    skill=request.POST.getlist('check2')
    c=[]

    for i in budget:
        a=project.objects.filter(payType= i)
        for j in a:
            c.append(j)
    for i in type:
        a = project.objects.filter(typeOfProject=i)
        for j in a:
            c.append(j)
    for i in skill:
        a = project.objects.filter(skills=i)
        for j in a:
            c.append(j)

    def Remove(duplicate):
        final_list = []
        for num in duplicate:
            if num not in final_list:
                final_list.append(num)
        return final_list

    c=Remove(c)
    return render(request,'Project/project.html',{"c":c})


def showBid(request,id):
    c = []
    c = project.objects.all()
    b=[]
    b=bid.objects.filter(proId_id=id)
    request.session['projectId']=id
    return render(request,'Project/showBid.html',{"c":c,"b":b,"id":id})

def search(request):
    name=request.POST.get('search','')
    c=project.objects.all()
    f=[]
    for p in c:
        n=p.skills
        if n.find(name)!=-1:
            f.append(p)

    return render(request,'Project/project.html',{"c":f})

def selectFreelancer(request,id):
    fid=bid.objects.get(id=id).freelancerName_id
    fre=freelancer.objects.get(id=fid)
    proj=project.objects.get(id=request.session['projectId'])
    proj.status='working'
    proj.finalSelection=fre.freelancerName
    if fre.numberOfProject>=3:
        return render_to_response('Employer/error.html')
    num_proj=fre.numberOfProject+1
    fre.numberOfProject=num_proj
    fre.save()
    proj.save()
    return render_to_response('Employer/loggedin.html')


