from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    #user management APIs.
    path('login/',csrf_exempt(login)),
    path('register/',csrf_exempt(registration)),
    path('update-user/',csrf_exempt(update_user)),
    path('users/',UserListView.as_view()),
    path('unassigned-users/',UnassignedUsers.as_view()),
    path('delete-user/<id>/',UserDeleteView.as_view()),
    path('roles/',RoleListView.as_view()),
    path('create-role/',RoleCreateView.as_view()),
    path('delete-role/<id>/',RoleDeleteView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
 
    
    #Files.
    # path('files/<int:staff_id>/',FileListView.as_view()),
    # path('Deletefile/<id>/', FileDeleteView.as_view()),


]

