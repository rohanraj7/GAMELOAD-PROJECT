from django.shortcuts import render,redirect
from django.contrib import messages
from gameadmin.models import User

# Create your views here.
def user(request):
    if request.user.is_authenticated and request.user.is_staff:

        ob = User.objects.all().order_by('id')
        context={'ob':ob}
        return render(request,'userlist.html',context)
    else:
        return redirect("/")

def block(request, id):
    obj = User.objects.values('active').get(id=id)
    if obj['active']==True:
        User.objects.filter(id=id).update(active=False)
        n='User Blocked'
        messages.info(request,n)
        return redirect('userlist')
    else:
        User.objects.filter(id=id).update(active=True)
        n = 'User Unblocked'
        messages.info(request,n)
        return redirect('userlist')