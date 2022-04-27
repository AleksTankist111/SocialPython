from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(Exercise)
admin.site.register(Record)
admin.site.register(User, UserAdmin)