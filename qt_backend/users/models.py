from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


# Create your models here.



class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self,email,names,phone,address,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError('Users must have a valid email')
        if not password:
            raise ValueError("You must enter a password")
        
        email=self.normalize_email(email)
        user_obj=self.model(email=email)
        user_obj.set_password(password)
        user_obj.names=names
        user_obj.phone=phone
        user_obj.address=address
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email,names,phone,address,password=None):
        user=self.create_user(email,names,phone,address,password=password,is_staff=True)
        return user

    def create_superuser(self,email,password=None):
        user=self.create_user(email,names="Admin admin",phone="0788888888",address="Kigali, Rwanda",password=password,is_staff=True,is_admin=True)
        return user
        

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    roles = models.ManyToManyField(Role,blank=True)
    names = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects= UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active



class Task(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_by  = models.ForeignKey('User',on_delete=models.CASCADE,blank=True,related_name="created_by")
    assignees  = models.ManyToManyField('User',blank=True,related_name="assignees")
    projects  = models.ManyToManyField('Project',blank=True)
    start_date = models.DateField(null=True, blank=True,default=timezone.now)
    end_date = models.DateField(null=True, blank=True,default=timezone.now)
    priority = models.CharField(max_length=100, null=True, blank=True)
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

class Project(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

class File(models.Model):
    task_id = models.ForeignKey('Task',on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to='media/',null=True,blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    
    
    
