# Generated by Django 2.1.5 on 2019-03-01 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposal', models.TextField(max_length=200)),
                ('price', models.IntegerField()),
                ('days', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='employers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EmployerName', models.CharField(max_length=50)),
                ('Password', models.CharField(max_length=50)),
                ('MobileNumber', models.IntegerField(max_length=10)),
                ('EmailId', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='freelancer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freelancerName', models.CharField(max_length=50)),
                ('skills', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=200)),
                ('review', models.TextField(max_length=500)),
                ('experience', models.CharField(max_length=500)),
                ('education', models.CharField(max_length=500)),
                ('qualifications', models.CharField(max_length=500)),
                ('profilePhoto', models.ImageField(upload_to='Files/')),
                ('password', models.CharField(max_length=10)),
                ('emailId', models.EmailField(max_length=254)),
                ('mobileNumber', models.IntegerField(max_length=10)),
                ('address', models.TextField(max_length=200)),
                ('certificates', models.FileField(upload_to='Files/')),
                ('bids', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=120)),
                ('files', models.FileField(upload_to='Files/')),
                ('skills', models.CharField(max_length=50)),
                ('typeOfProject', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('payType', models.CharField(max_length=30)),
                ('bidNumber', models.IntegerField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('EmpId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.employers')),
            ],
        ),
        migrations.AddField(
            model_name='bid',
            name='freelancerName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.freelancer'),
        ),
        migrations.AddField(
            model_name='bid',
            name='proId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.project'),
        ),
    ]
