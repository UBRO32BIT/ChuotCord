from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50)

# Represents the users in groups (M-M)
class GroupUser(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=100, null=True)

    class Meta:
        # Composite primary key
        unique_together = (('group', 'member'),)

class MessageGroup(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now=True)