from django.urls import path
from .views import users_list
from enrolment import views
# URL Config
urlpatterns = [
	path('users_list/<int:id>',views.users_list),
]