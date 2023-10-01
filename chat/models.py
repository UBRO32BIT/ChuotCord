from django.db import models
from django.contrib.auth.models import User
import random
import string

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id}. {self.name}"

# Represents the users in groups (M-M)
class GroupUser(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=100, null=True)
    def __str__(self):
        return f"User {self.member.username} in Group ID {self.group.id}"
    class Meta:
        # Composite primary key
        unique_together = (('group', 'member'),)
        indexes = [
            models.Index(fields=['member', 'group']),
        ]

# Represents messages sent by user in groups
class MessageGroup(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images', blank=True)


def generate_random_string(length):
    # Define the characters you want to use for generating the random string
    characters = string.ascii_letters + string.digits  # Use letters and digits

    # Generate a random string of the specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

# Represents invitations created by user
class Invite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    string = models.CharField(
        max_length=10,
        editable=False,
        unique=True,
        default=generate_random_string(10)
        )
    created_at = models.DateTimeField(auto_now=True)
    expiry = models.DateTimeField(null=True)