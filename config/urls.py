from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # Admin URLS
    path('admin/', admin.site.urls),
    
    #Auth URLS
    path('api/', include('authentication.urls')),
    path('enrolment/', include('enrolment.urls')),
]
