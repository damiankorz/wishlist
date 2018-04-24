from __future__ import unicode_literals
from django.db import models
import bcrypt 

class UserManager(models.Manager):
    def register_validator(self, request):
        errors = []
        if request.method == 'POST':
            if len(request.POST['name']) < 3:
                errors.append('Name must be at least three characters long')
            if len(request.POST['username']) < 3:
                errors.append('Username must be at least three characters long') 
            if len(request.POST['password']) < 8:
                errors.append('Password must be at least eight characters long')
            if request.POST['confirm_password'] != request.POST['password']:
                errors.append('Passwords did not match')
            if request.POST['date_hired'] == '':
                errors.append('Enter valid date as MM/DD/YYYY')
            users = User.objects.all()
            for user in users: 
                if request.POST['username'] == user.username:
                    errors.append('Username already exists')
            return errors
    def register_user(self, request):
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed_pw, date_hired=request.POST['date_hired'])
    def login_validator(self, request):
        if request.method == 'POST':
            errors = []
            users = User.objects.filter(username=request.POST['username'])
            if len(users) > 0:
                user = users[0]
                if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                    request.session['logged_id'] = user.id
                    return errors
                else: 
                    errors.append('Incorrect Password')
                    return errors
            else: 
                errors.append('Username not found (username is case sensitive)')
                return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class ItemManager(models.Manager):
    def item_validator(self, request):
        if request.method == 'POST':
            errors = []
            if len(request.POST['item']) < 4:
                errors.append('Item/Product name must be at least four characters long')
            return errors
    def item_create(self, request):
        Item.objects.create(name=request.POST['item'], user_id=request.session['logged_id'])
    def item_delete(self, request, id):
        item = Item.objects.get(id=id)
        item.delete()
    def item_on_wishlist(self, request, id):
        full_list = []
        creators_list = Item.objects.filter(id = id)
        wishers_list = List.objects.filter(items_id = id)
        for creator in creators_list:
            if creator.user.name not in full_list:
                full_list.append(creator.user.name)
        for wisher in wishers_list:
            if wisher.wishers.name not in full_list:
                full_list.append(wisher.wishers.name)
        return full_list

class Item(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()

class ListManager(models.Manager):
    def add_to_wishList(self, request, id):
        List.objects.create(items_id=id, wishers_id=request.session['logged_id'])
    def remove_from_wishList(self, request, id):
        list_object = List.objects.get(id=id)
        list_object.delete()
        
class List(models.Model):
    items = models.ForeignKey(Item, related_name="items")
    wishers = models.ForeignKey(User, related_name="wishers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ListManager()