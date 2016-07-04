from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from post.models import PostModel
# Create your views here.


def register(request): 
    if request.method == 'POST': 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            new_user = form.save()

            #Assign the new user to the students group
            student_group = Group.objects.get(name='students')
            new_user.groups.add(student_group)

            #Bypass authentication requirement
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, new_user)
            return redirect('/accounts/profile/')

    if request.method == 'GET':
        form = UserCreationForm()
    context = {'form': form}
    context.update(csrf(request))       
    return render(request, "accounts/register.html", context)

@login_required
def profile(request):
    
    if request.user.groups.filter(name='students').exists():
        #Students see their own posts
    	context = {}
    	context['posts'] = request.user.owner.all()
    	return render(request, 'accounts/student_profile.html', context)

    elif request.user.groups.filter(name='staff').exists() or request.user.is_superuser:
        #Staff see their own posts and all the students' posts
        context = {}                  
        context['own_posts'] = request.user.owner.all()
        context['students'] = Group.objects.get(name='students').user_set.all()
        student_posts = {}
        for student in context['students']:
            #Only submitted posts can be seen.
            student_posts[student.username] = student.owner.filter(status='post')
        context['student_posts'] = student_posts
        return render(request, 'accounts/staff_profile.html', context)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
        	login(request, form.get_user())
        	return redirect('/accounts/profile/')
    if request.method == 'GET':
    	form = AuthenticationForm(request)
    context = {'form': form}
    context.update(csrf(request))
    return render(request, 'accounts/login.html', context)

def user_logout(request):
	logout(request)
	return render(request, 'accounts/logout.html')