from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Branch)
admin.site.register(School)
admin.site.register(Family)
admin.site.register(Medical)
admin.site.register(Student)
admin.site.register(student_enroll)
