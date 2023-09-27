from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views import View
from .models import MessageGroup, Group, GroupUser, Invite
from .forms import CreateGroupForm

def is_chat_member(user, group_id):
    return user.is_authenticated and GroupUser.objects.filter(group=group_id, member=user).exists()

class ChatView(View):
    def get(self, request, group_id):
        # Get current user
        current_user = request.user
        # If the user is not authorized
        if (not is_chat_member(current_user, group_id)):
            return HttpResponseNotAllowed("You do not have permission to access this resource.")
        
        group = get_object_or_404(Group, id=group_id)
        context = {
            'chat_messages': MessageGroup.objects.filter(group=group),
            'group': group,
            'members': GroupUser.objects.filter(group=group)
        }
        return render(request, "chat/chat.html", context)
    

class CreateChatView(View):
    def get(self, request):
        context = {"form": CreateGroupForm()}
        return render(request, "chat/group/create.html", context)
    
    def post(self, request):
        name = request.POST.get("name")
        group = Group(name=name, owner=request.user)
        group.save()
        # Add the user to the chat room
        group_user = GroupUser(group=group, member=request.user, alias=None)
        group_user.save()
        messages.info(request, 'Added group successfully!')
        return redirect('home')
    
class DeleteChatView(View):
    def get(self, request, group_id):
        user = request.user
        
        group = get_object_or_404(Group, id=group_id)
        if group.owner != user:
            return HttpResponseNotAllowed("You do not have permission to access this resource.")
        
        context = {"name": group.name}
        return render(request, "chat/group/delete.html", context)

    def post(self, request, group_id):
        user = request.user
        if not user.is_authenticated:
            messages.error(request, 'You must log in to continue!')
            return redirect('login')
        
        group = get_object_or_404(Group, id=group_id)
        if group.owner != user:
            return HttpResponseNotAllowed("You do not have permission to access this resource.")
        
        group.delete()
        messages.success(request, 'Deleted group successfully!')
        return redirect('home')
    

class AddUserToGroupView(View):
    def get(self, request, invite_str):
        invite = get_object_or_404(Invite, string=invite_str)
        page = "invite/invite.html"
        
        if invite.expiry < timezone.now():
            # Check if the invite has expired
            page = "invite/invite_expired.html"
        else:
            user = request.user
            group = invite.group
            if is_chat_member(user, group.pk):
                messages.error(request, "You are already a member of this group!")
                return redirect('chat', group_id=group.pk)
        
        context = dict()
        context['group_name'] = group.name
        return render(request, page, context)
    
    def post(self, request, invite_str):
        invite = get_object_or_404(Invite, string=invite_str)
        if (invite.expiry < timezone.now()):
            # Check if the invite has expired
            render(request, "invite/invite_expired.html")
        else:
            user = request.user
            group = invite.group
            if is_chat_member(user, group.pk):
                messages.error(request, "You are already a member of this group!")
                return redirect('chat', group_id=group.pk)
        
        # Add the user to the group
        GroupUser.objects.create(group=group, member=user, alias=None)  # You can set an alias here if needed

        return redirect('chat', group_id=group.pk)