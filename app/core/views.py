from django.shortcuts import render

# Create your views here.
# New Code
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.db import IntegrityError 
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from.models import Todo
from django.utils import timezone 
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'core/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except:
            return render(request, 'core/createtodo.html', {'form':TodoForm(), 'error':'Bad Data, please try again'})

@login_required
def completetodo(request, todo_pk):
    
    todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)

    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    
    todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)

    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def viewtodo(request, todo_pk):

    todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)    

    if request.method == 'GET':
        form = TodoForm(instance=todo) 
        return render(request, 'core/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try: 
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'core/viewtodo.html', {'todo':todo, 'form':form, 'error':'Save failed, please try again'})

@login_required
def currenttodos(request):
        todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
        return render(request, 'core/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
        todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
        return render(request, 'core/completedtodos.html', {'todos':todos})

def signupuser(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('currenttodos')
        else:
            return render(request, 'core/signupuser.html', {'form':UserCreationForm()})
    else:
        # Create user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'core/signupuser.html', {'form':UserCreationForm(), 'error':'Duplicate username'})
        else:
            return render(request, 'core/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords must match'})
          
def loginuser(request):

    if request.method == 'GET':
        return render(request, 'core/loginuser.html', {'form':AuthenticationForm()})
    else:
       user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
       if user is None:
            return render(request, 'core/loginuser.html', {'form':AuthenticationForm(), 'error':'User name and password did not match'})
       else:
            login(request, user)
            return redirect('currenttodos')

def logoutuser(request):

    if request.method == 'POST':
        logout(request)
        return redirect('home')

def home(request):
        return render(request, 'core/home.html')
