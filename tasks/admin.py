from django.contrib import admin

# Register your models here.
from .models import Task, Priority

admin.site.register(Task)
admin.site.register(Priority)
