from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import MessageGroup, Group, GroupUser
# Create your views here.
def chat(request, group_id):
    current_user = request.user
    if (request.method == 'GET'):
        group = Group.objects.get(id=group_id)
        context = dict()
        context['messages'] = MessageGroup.objects.filter(group=group)
        context['group'] = group
        context['members'] = GroupUser.objects.filter(group=group)
        return render(request, "chat/chat.html", context)