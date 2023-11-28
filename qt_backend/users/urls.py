from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    #user management APIs.
    path('login/',csrf_exempt(login)),
    path('register/',csrf_exempt(registration)),
    path('update-user/',csrf_exempt(update_user)),
    path('users/',UserListView.as_view()),
    path('delete-user/<id>/',UserDeleteView.as_view()),
    path('roles/',RoleListView.as_view()),
    path('create-role/',RoleCreateView.as_view()),
    path('delete-role/<id>/',RoleDeleteView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),

    #Projects APIs.
    path('projects/', ProjectListView.as_view()),

    #Tasks APIs.
    path('tasks/',TaskListView.as_view()),
    path('task-delete/<id>/',TaskDeleteView.as_view()),
    path('task-create/',csrf_exempt(create_task)),
    path('task-update/<id>/',TaskUpdateView.as_view()),
 
    
    #Files APIs.
    path('files/<int:task_id>/',FileListView.as_view()),


]

