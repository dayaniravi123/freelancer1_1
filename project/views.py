from django.shortcuts import render, render_to_response
from employer.models import project, bid,freelancer


def show(request):
    c=[]
    c=project.objects.all()
    b=[]
    b=bid.objects.all()
    return render(request,'Project/project.html',{"c":c,"b":b})

def showBid(request,id):
    c = []
    c = project.objects.all()
    b=[]
    b=bid.objects.filter(proId_id=id)
    request.session['projectId']=id
    return render(request,'Project/showBid.html',{"c":c,"b":b,"id":id})

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


