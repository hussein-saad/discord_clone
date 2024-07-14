from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic, Message,User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .forms import RoomForm, UserForm, CustomUserCreationForm


def login_page(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'username or password does not exits') 
    context = {'page': page}
    return render(request, 'base/login_register.html',context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
        
    if request.user.is_authenticated:
        return redirect('home')
    
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')
    
    context = {'form': form}
    return render(request, 'base/login_register.html',context)
    


def home(request): 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) | 
        Q(description__icontains=q)
        )
    
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    
    room_messages = Message.objects.filter(room__topic__name__icontains=q)
    
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'base/home.html',context)


def room(request, id):
    room = Room.objects.get(id=id)
    room_messages = room.message_set.all().order_by('-created_at')
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        
        room.participants.add(request.user)
        
        return redirect('room', id=room.id)
    
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html',context)


def user_profile(request,id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
    }
    return render(request, 'base/profile.html',context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        
        topic_name = request.POST.get('topic')
        
        topic,created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('home')
    
    context = {
        'form': form,
        'topics': topics,
    }
    
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def update_room(request, id):
    room = Room.objects.get(id=id)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    form = RoomForm(instance=room)
    
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')
    
    context = {
        'form': form,
        'room': room,
        'topics': topics,
    }
    return render(request, 'base/room_form.html',context) 

@login_required(login_url='login')
def delete_room(request, id):
    room = Room.objects.get(id=id)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj' : room}) 


def delete_message(request,id):
    message = Message.objects.get(id=id)
    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj' : message})

@login_required(login_url='login')    
def update_user(request):
    form = UserForm(instance=request.user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile',id=request.user.id)
    
    context = {
        'form': form
    }
    
    return render(request, 'base/update_user.html',context)

def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {
        'topics':topics,
    }
    return render(request, 'base/topics.html',context)

def activity_page(request):
    room_messages = Message.objects.all()
    context = {
        'room_messages':room_messages,
    }
    return render(request, 'base/activity.html',context)