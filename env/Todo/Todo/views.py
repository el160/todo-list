from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import TODO  
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
def signup(request):
    if request.method=='POST':
        ljh = request.POST.get('ljh')
        emailid = request.POST.get('email')
        pwd = request.POST.get('pwd')
        
        # Check if username exists
        if User.objects.filter(username=ljh).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})
        
        # Create user
        my_user = User.objects.create_user(username=ljh, email=emailid, password=pwd)
        my_user.save()
        return redirect('/login')
    
    return render(request, 'signup.html')

def loginn(request):
    if request.method=='POST':
        ljh = request.POST.get('ljh')
        pwd = request.POST.get('pwd')
        print(ljh, pwd)
        # # Authenticate user
        user = authenticate(request,username=ljh, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/todopage')
        else:
            return redirect('/login')

    return render(request, 'login.html')
        
        
@login_required(login_url='/loginn')
def todo(request):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        object=TODO(title=title,user=request.user)
        object.save()
        res=TODO.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage',{'res':res})
    res=TODO.objects.filter(user=request.user).order_by('-date')
    return render(request,'todo.html',{'res':res})



@login_required(login_url='/loginn')
def edit_todo(request,srno):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        object=TODO.objects.get(srno=srno)
        object.title=title
        object.save()
        user=request.user
        
        return redirect('/todopage',{"object":object})
    object=TODO.objects.get(srno=srno)
    
    return render(request,'todo.html')
    

@login_required(login_url='/loginn')
def delete_todo(request,srno):
    object=TODO.objects.get(srno=srno)
    object.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/login')
    