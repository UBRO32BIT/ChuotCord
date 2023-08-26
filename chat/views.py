from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import MessageGroup, Group, GroupUser
# Create your views here.
def chat(request, group_id):
    # Get current user
    current_user = request.user
    # If the user is not authenticated
    if (not current_user.is_authenticated):
        messages.error(request, ('You must login to send a message!'))
        return redirect('login')
    # GET method
    if (request.method == 'GET'):
        group = Group.objects.get(id=group_id)
        context = dict()
        context['messages'] = MessageGroup.objects.filter(group=group)
        context['group'] = group
        context['members'] = GroupUser.objects.filter(group=group)
        return render(request, "chat/chat.html", context)