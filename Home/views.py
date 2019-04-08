from _datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from employer.models import project, bid, employers, Feedback


# Create your views here.
def display(request):
    c=[]
    c=project.objects.all()
    b=[]
    b=bid.objects.all()
    cDate=datetime.now()
    cDate=cDate.strftime('%Y-%m-%d')
    for pro in c:
        proDate=datetime.strptime(pro.endDate,'%Y-%m-%d')
        proDate=proDate.strftime('%Y-%m-%d')
        if proDate==cDate:
            subject = "Bidding"
            message = "\n\nYour bidding date is completed so choose one of Freelancer. \n\n-Employment Hub.\n"
            # from_email = settings.EMAIL_HOST_USER
            emp=employers.objects.get(id=pro.EmpId_id)
            to_list =[emp.EmailId]
            send_mail(subject, message, 'freelancerdjango@gmail.com', to_list)

    return render(request,'Home/home.html',{"c":c,"b":b})

