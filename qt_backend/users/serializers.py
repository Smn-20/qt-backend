from rest_framework import serializers

from .models import *

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'names', 'phone', 'address', 'is_active', 'is_staff', 'is_admin','created_at', 'roles')
        

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['roles'] is not None:
            roles = []
            for role in data['roles']:
                obj = RoleSerializer(
                Role.objects.get(pk=role)).data
                roles.append(obj)
            data['roles']=roles
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    oldPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =('id', 'created_by','name','description','assignees', 'projects','start_date','end_date','priority','started','completed')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['created_by'] is not None:
            data['created_by'] = UserSerializer(
                User.objects.get(pk=data['created_by'])).data
        if data['assignees'] is not None:
            assignees = []
            for assignee in data['assignees']:
                obj = UserSerializer(
                User.objects.get(pk=assignee)).data
                assignees.append(obj)
            data['assignees']=assignees
        if data['projects'] is not None:
            projects = []
            for project in data['projects']:
                obj = ProjectSerializer(
                Project.objects.get(pk=project)).data
                projects.append(obj)
            data['projects']=projects
        return data

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'task_id', 'file', 'name', 'type', 'size', 'created_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['task_id'] is not None:
            data['task_id'] = TaskSerializer(
                Task.objects.get(pk=data['task_id'])).data
        return data



    

