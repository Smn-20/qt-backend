from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView,DestroyAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from django.http import Http404, HttpResponse,JsonResponse
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import secrets
import string
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
from rest_framework.permissions import IsAuthenticated 
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from django.utils.timezone import now
from datetime import datetime, timedelta
import math


# Create your views here.
def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        try:
            user = User.objects.get(email=body['email'])
            if user.check_password(body['password']):
                token = Token.objects.get_or_create(user=user)[0]
                data = {
                    'user_id': user.id,
                    'email': user.email,
                    'status': 'success',
                    'roles':str(list(user.roles.values_list('name', flat=True))),
                    'token': str(token),
                    'code': status.HTTP_200_OK,
                    'message': 'Login successfull',
                    'data': []
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
            else:
                data = {
                    'status': 'failure',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Email or password incorrect!',
                    'data': []
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
        except User.DoesNotExist:
            data = {
                'status': 'failure',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Email or password incorrect!',
                'data': []
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type='application/json')

def registration(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        try:
            user=User.objects.get(email=body['email'])
            data = {
                'status':'false',
                'message': 'A user with this email already exists!',
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type='application/json')
        except User.DoesNotExist:
            try:
                user=User.objects.get(phone=body['phone'])
                data = {
                    'status':'false',
                    'message': 'A user with this phone number already exists!',
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
            except User.DoesNotExist:
                user=User.objects.create_user(
                    email=body['email'],
                    names=body['names'],
                    phone=body['phone'],
                    address=body['address'],
                    password=body['password'],
                    )
                for role in body['roles']:
                    role=Role.objects.get(id=role)
                    user.roles.add(role)
                
                user.save()
                data = {
                    'status':'true',
                    'message': 'Registered successfully!!',
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')

def update_user(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        email = User.objects.get(id=body['id']).email
        phone = User.objects.get(id=body['id']).phone
        if body['email']!=email or body['phone']!=phone:
            try:
                if body['email']!=email and body['phone']!=phone:
                    user=User.objects.get(email=body['email']) or User.objects.get(phone=body['phone'])
                    data = {
                        'status':'false',
                        'message': 'A user with this email or phone already exists!',
                    }
                    dump = json.dumps(data)
                    return HttpResponse(dump, content_type='application/json')
                else:
                    if body['email']!=email and body['phone'] == phone:
                        user=User.objects.get(email=body['email'])
                        data = {
                            'status':'false',
                            'message': 'A user with this email already exists!',
                        }
                        dump = json.dumps(data)
                        return HttpResponse(dump, content_type='application/json')

                    if body['email']==email and body['phone'] != phone:
                        user=User.objects.get(phone=body['phone'])
                        data = {
                            'status':'false',
                            'message': 'A user with this phone already exists!',
                        }
                        dump = json.dumps(data)
                        return HttpResponse(dump, content_type='application/json')
            except User.DoesNotExist:
                user=User.objects.get(id=body['id'])
                user.email=body['email']
                user.names=body['names']
                user.phone=body['phone']
                user.address=body['address']
                user.roles.clear()
                user.save()
                for role in body['roles']:
                    role=Role.objects.get(id=role)
                    user.roles.add(role)
                
                user.save()
                data = {
                    'status':'true',
                    'message': 'Updated successfully!!',
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
            
        else:
            user=User.objects.get(id=body['id'])
            user.email=body['email']
            user.names=body['names']
            user.phone=body['phone']
            user.address=body['address']
            user.roles.clear()
            user.save()
            for role in body['roles']:
                role=Role.objects.get(id=role)
                user.roles.add(role)
            
            user.save()
            data = {
                'status':'true',
                'message': 'Updated successfully!!',
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type='application/json')

class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("oldPassword")):
                return Response({"message":"Old/Current password incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("newPassword"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#User
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    
class RoleListView(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleCreateView(CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleDeleteView(DestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'id'

class TaskListView(ListAPIView):
    serializer_class = TaskSerializer
    def get_queryset(self):
        created_tasks = Task.objects.filter(created_by=self.request.user.id)
        assigned_tasks = Task.objects.filter(assignees__in=[self.request.user.id])
        tasks = created_tasks | assigned_tasks
        return tasks

class TaskDeleteView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

def create_task(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        
        

        created_by = User.objects.get(id=request.POST['created_by'])

        # Create the company
        task = Task.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            created_by=created_by,
            start_date=request.POST['startDate'],
            end_date=request.POST['endDate'],
            priority=request.POST['priority'],
            
        )
        task.save()

        for assignee in request.POST['assignees']:
            assignee=User.objects.get(id=assignee)
            task.assignees.add(assignee)

        task.save()

        for project in request.POST['projects']:
            project=Project.objects.get(id=project)
            task.projects.add(project)

        task.save()

        

        for file in files:
            File.objects.create(
                task_id=task,
                file=file,
                name=file.name,
                type=file.content_type,
                size=file.size
            )
    

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



class TaskUpdateView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

def update_task(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body['name'])
        # Create the company
        
        task = Task.objects.get(id=body['taskId'])
        task.name=body['name'],
        task.description=body['description'],
        # task.start_date=body['startDate'],
        # task.end_date=body['endDate'],
        task.priority=body['priority'],
            
        task.assignees.clear()
        task.projects.clear()

        if body['status']:
            if body['status'] == "started":
                task.started = True
            if body['status'] == "completed":
                task.completed = True

        task.save()

        for assignee in body['assignees']:
            assignee=User.objects.get(id=assignee)
            task.assignees.add(assignee)

        task.save()

        for project in body['projects']:
            project=Project.objects.get(id=project)
            task.projects.add(project)

        task.save()

    
    

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

class ProjectListView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    
class FileListView(ListAPIView):
    serializer_class = FileSerializer
    def get_queryset(self):
        files = File.objects.filter(task_id=self.kwargs['task_id'])
        return files
