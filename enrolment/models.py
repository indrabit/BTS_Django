
import email
from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    accountname=models.CharField(max_length=50,blank=False)
    bsb=models.CharField(max_length=6)
    accountno=models.CharField(max_length=10)
    
    
    listed = models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.name
    
class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=100,blank=True)
    address = models.CharField(max_length=100,blank=True)
    suburb = models.CharField(max_length=50,blank=False)
    state=models.CharField(max_length=4,blank=False)
    postcode=models.CharField(max_length=4,blank=False)
    email=models.EmailField(max_length=50,blank=True)
    contactno=models.CharField(max_length=50,blank=True)
    branch = models.ForeignKey(School,on_delete=models.CASCADE,)
    listed = models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.name
    
class Family(models.Model):
    
    FATHER='f',
    MOTHER='m'
    BROTHER='b'
    SISTER='s'
    UNCLUE='u'
    
    PARENT_CHOICES=(
        ('FATHER','Father'),
        ('MOTHER','Mother'),
        ('BROTHER','Brother'),
        ('SISTER','Sister'),
        ('UNCLE','Uncle')
    )
    

    parent_type=models.CharField(max_length=20,choices=PARENT_CHOICES)
    PROF = 1
    DR = 2
    MR = 3
    MRS = 4
    MS = 5
    PROFESSION_TITLE = ((PROF, 'Prof.'),
                        (DR, 'Dr.'),
                        (MR, 'Mr'),
                        (MRS, 'Mrs'),
                        (MS, 'Ms'),)
    
    title = models.IntegerField(choices=PROFESSION_TITLE, blank=True, null=True)
    first_name =models.CharField(max_length=50,null=False)
    last_name = models.CharField(max_length=50,null=False)
    mobile=models.CharField(max_length=50,null=False)
    email=models.CharField(max_length=50,null=False)
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.first_name +' '+self.last_name
    
class Medical(models.Model):
    dr_name=models.CharField(max_length=50,null=False)
    address=models.CharField(max_length=50,null=False)
    suburb=models.CharField(max_length=50,blank=False)
    state=models.CharField(max_length=4,blank=False)
    postcode=models.CharField(max_length=50,blank=False)
    telephone=models.CharField(max_length=20,blank=False)
    def __str__(self) -> str:
        return self.first_name +' '+self.last_name
    
class Student(models.Model):
    first_name =models.CharField(max_length=50,null=False)
    last_name = models.CharField(max_length=50,null=False)
    dob=models.DateField(max_length=15)
    
    MALE='m',
    FEMALE='f'
    OTHER='o'
    STATUS_CHOICES=(
        ('MALE','Male'),
        ('FEMALE','Female'),
        ('OTHER','Other')
    )
    
    sex=models.CharField(max_length=10,choices=STATUS_CHOICES)
    CITIZEN = 1
    PERMANENT = 2
    WORKING = 3
    STUDENT = 4
    TRAVEL = 5
    RESIDENTAL_STATUS = ((CITIZEN, 'Australian Citizenship'),
                        (PERMANENT, 'Permanent Resident.'),
                        (WORKING, 'Working Visa'),
                        (STUDENT, 'Student Visa'),
                        (TRAVEL, 'Travel Visa'),)
    
    
    residental_status=models.CharField(max_length=50,choices=RESIDENTAL_STATUS)
    mains_school_name=models.CharField(max_length=50,null=True)
    mains_school_class=models.CharField(max_length=5,null=True)
    mains_school_address=models.CharField(max_length=50,null=True)    
    mains_schoolsuburb=models.CharField(max_length=50,blank=False)
    mains_schoolstate=models.CharField(max_length=10,blank=False)
    mains_school_postcode=models.CharField(max_length=10,blank=False)
    medical=models.ForeignKey(to=Medical,on_delete=models.CASCADE)
    parent=models.ForeignKey(to=Family,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.first_name +' '+self.last_name

    
class student_enroll(models.Model):
    enroll_date=models.DateField(max_length=10,blank=False)

    FULL='f',
    NO='n'
    PARTIAL='p'
    PAYMENT_TYPE=(
        ('FULL','Full'),
        ('NO','No'),
        ('PARTIAL','Partial')
    )
    paid = models.CharField(max_length=10,choices=PAYMENT_TYPE)
    student=models.ForeignKey(to=Student,on_delete=models.CASCADE)
    school=models.ForeignKey(to=School,on_delete=models.CASCADE)
    term_condition_accept=models.BooleanField(default=False)
    declaration=models.BooleanField(default=False)
  
    