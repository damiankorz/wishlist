from django.shortcuts import render, redirect
from django.contrib import messages 
from models import *

#index ('localhost:8000/') redirects to main
def index(request):
    return redirect('/main')

def main(request):
    if 'logged_id' not in request.session:
        return render(request, 'users/main.html')
    else: 
        return redirect('/dashboard')

def dash(request):
    if 'logged_id' not in request.session:
        return redirect('/main')
    context = {
        'user': User.objects.get(id=request.session['logged_id']),
        'items': Item.objects.exclude(items__wishers_id=request.session['logged_id']),
        'wishersList': List.objects.filter(wishers_id=request.session['logged_id']),
    }
    return render(request, 'users/dashboard.html', context)

def login(request):
    errors = User.objects.login_validator(request)
    if len(errors):
        for error in errors:
            messages.error(request, error)
            return redirect('/main')
    else:
        return redirect('/dashboard')

def register(request):
    errors = User.objects.register_validator(request)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/main')
    else: 
        User.objects.register_user(request)
        request.session['logged_id'] = User.objects.last().id
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def create(request):
    return render(request, 'users/create.html')

def process(request):
    errors = Item.objects.item_validator(request)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/wish_items/create')
    else:
        Item.objects.item_create(request)
        return redirect('/dashboard')

#display item page 
def display_item(request, id):
    context = {
        'item': Item.objects.get(id=id),
        'full_list': Item.objects.item_on_wishlist(request, id)
    }
    return render(request, 'users/item.html', context)

#delete item from database
def delete(request, id):
    Item.objects.item_delete(request, id)
    return redirect('/dashboard')

#add to my list
def add(request, id):
    List.objects.add_to_wishList(request, id)
    return redirect('/main')

#remove from my list
def remove(request, id):
    List.objects.remove_from_wishList(request, id)
    return redirect('/main')
