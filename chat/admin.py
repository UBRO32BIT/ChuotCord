from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Group)
admin.site.register(models.GroupUser)
admin.site.register(models.MessageGroup)