from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import MessageGroup, Group, GroupUser
from .forms import CreateGroupForm
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
    
def create_chat(request):
    current_user = request.user
    if (not current_user.is_authenticated):
        messages.error(request, ('You must login to create a new group!'))
        return redirect('login')
    
    if (request.method == 'GET'):
        context = dict()
        context["form"] = CreateGroupForm()
        return render(request, "chat/group/create.html", context)
    if (request.method == 'POST'):
        name = request.POST["name"]
        group = Group(name=name, owner=current_user)
        group.save()
        # Add the user in the chat room
        group_user = GroupUser(group=group, member=current_user, alias=None)
        group_user.save()
        messages.info(request, ('Added group successfully!'))
        return redirect('home')

