from django.shortcuts import render,redirect
from .models import *



def get_user(request):
    return request.user.id


def home(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        room_code = request.POST.get('room_code')
        
        room_obj, _ = Room.objects.get_or_create(room_code=room_code)
        
        print(room_obj)
        return redirect(f'/chat/{room_code}/?username={username}')
    return render(request , 'home.html')

def chat(request,room_code):
    return render(request , 'chat.html')