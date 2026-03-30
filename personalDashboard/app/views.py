from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item

def auth_view(request):
    return render(request, 'auth.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'auth.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        if p1 != p2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth.html', {'show_register': True})
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'auth.html', {'show_register': True})
        User.objects.create_user(username=username, password=p1)
        messages.success(request, 'Account created! Please log in.')
        return redirect('login')
    return render(request, 'auth.html', {'show_register': True})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    items = Item.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'items': items})

@login_required
def item_create(request):
    if request.method == 'POST':
        Item.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description')
        )
    return redirect('dashboard')

@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    if request.method == 'POST':
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.save()
    return redirect('dashboard')

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
    return redirect('dashboard')