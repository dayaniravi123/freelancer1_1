from django.db import models

class employers(models.Model):
    EmployerName=models.CharField(max_length=50)
    Password=models.CharField(max_length=50)
    MobileNumber=models.IntegerField(max_length=10)
    EmailId=models.EmailField(max_length=254)

class project(models.Model):
   projectName=models.CharField(max_length=50)
   EmpId=models.ForeignKey(employers,on_delete=models.CASCADE)
   description=models.TextField(max_length=120)
   files=models.FileField(upload_to="Files/",max_length=100)
   skills=models.CharField(max_length=50)
   typeOfProject=models.CharField(max_length=50)
   price=models.IntegerField()
   payType=models.CharField(max_length=30)
   bidNumber=models.IntegerField()
   startDate=models.CharField(max_length=30)
   endDate=models.CharField(max_length=30)
   status=models.CharField(max_length=30,default='incomplete')
   finalSelection=models.CharField(max_length=50,default='none')
   team=models.CharField(max_length=20,default='No')

class freelancer(models.Model):
    freelancerName=models.CharField(max_length=50)
    skills=models.CharField(max_length=100)
    description=models.TextField(max_length=200)
    review=models.TextField(max_length=500)
    experience=models.CharField(max_length=500)
    education=models.CharField(max_length=500)
    qualifications=models.CharField(max_length=500)
    profilePhoto=models.ImageField(upload_to="Files/")
    password=models.CharField(max_length=10)
    emailId=models.EmailField(max_length=254)
    mobileNumber=models.IntegerField(max_length=10)
    address=models.TextField(max_length=200)
    certificates=models.FileField(upload_to="Files/")
    bids=models.IntegerField()
    paytmLink=models.CharField(default='none',max_length=50)
    numberOfProject=models.IntegerField(default=0)

class freelancerTeam(models.Model):
    memberName=models.CharField(max_length=50)
    experience=models.IntegerField()
    mobileNo=models.IntegerField()
    freelancer=models.ForeignKey(freelancer,on_delete=models.CASCADE)

class bid(models.Model):
    freelancerName=models.ForeignKey(freelancer,on_delete=models.CASCADE)
    proposal=models.TextField(max_length=200)
    price=models.IntegerField()
    days=models.IntegerField()
    team=models.CharField(default='No',max_length=10)
    proId=models.ForeignKey(project,on_delete=models.CASCADE)

