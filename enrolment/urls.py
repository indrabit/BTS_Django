from django.urls import path
from .views import users_list,handleUpdate
from enrolment import views
# URL Config
urlpatterns = [
	path('users_list/<int:id>',views.users_list),
	path(r'updateProfile/<int:id>', views.handleUpdate, name="handleUpdate")
]