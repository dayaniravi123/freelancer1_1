# Generated by Django 2.1.5 on 2019-04-05 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0014_freelancerteam_dept'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Subject', models.CharField(max_length=50)),
                ('Email', models.CharField(max_length=50)),
                ('Message', models.CharField(max_length=200)),
            ],
        ),
    ]