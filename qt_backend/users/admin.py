from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *



User=get_user_model()

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(File)





# Register your models here.
