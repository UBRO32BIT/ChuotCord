from django.shortcuts import render, redirect
from chat.models import GroupUser, Group

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
        groups = GroupUser.objects.filter(member_id=user.id)
        context = {
            "groups": groups
            }
        return render(request, "index.html", context)
    else:
        # Handle the case when the user is not authenticated
        # For example, you can redirect them to a login page.
        # Or provide a message indicating they need to log in.
        # Adjust this part based on your application's logic.
        return redirect('login')