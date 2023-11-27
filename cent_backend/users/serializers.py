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

# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
        
# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         fields = ('id','staff_id','file','name','type','extension','size','created_at')

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         if data['staff_id'] is not None:
#             data['staff_id'] = StaffSerializer(
#                 Employees.objects.get(pk=data['staff_id'])).data
#         return data



    

