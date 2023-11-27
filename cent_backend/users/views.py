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
#User
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UnassignedUsers(ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(employees__isnull=True)

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



# class FileListView(ListAPIView):
#     serializer_class = FileSerializer
#     def get_queryset(self):
#         return File.objects.filter(staff_id=self.kwargs['staff_id'])



# class FileDeleteView(DestroyAPIView):
#     queryset = File.objects.all()
#     serializer_class = FileSerializer
#     lookup_field = 'id'
    
    
