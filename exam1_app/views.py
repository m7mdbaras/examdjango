from django.shortcuts import render, redirect
from django.http import request
from django.contrib import messages
from .models import User
from .models import Item
import bcrypt

# Create your views here.
def index(request):
    return render(request, "login.html")

def register(request):
    validationErrors = User.objects.regValidator(request.POST)
    if len(validationErrors) > 0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashedPw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(
            f_name = request.POST['f_name'], 
            l_name = request.POST['l_name'], 
            email = request.POST['email'], 
            password = hashedPw
        )
        request.session['uuid'] = newUser.id 
        
        return redirect('/dashboard')

def dashboard(request):
    if 'uuid' not in request.session:
        messages.error(request, "You must have an acount!")
        return redirect('/')
    

    all_wishes = Item.objects.all()
    user_wishes = Item.objects.all().filter(wisher = request.session['uuid'] )
    granted_wishes = all_wishes.exclude(date_granted = None)
    not_granted = user_wishes.filter(date_granted = None)
    
    context = {
        'granted' : granted_wishes,
        'wishes': not_granted,
        'loggedInUser': User.objects.get(id = request.session['uuid']),
        'all_wishes' : Item.objects.all(),
    }
    return render(request, "dashboard.html", context)

def login(request):
    loginErrors = User.objects.loginValidator(request.POST)
    if len(loginErrors) > 0: 
        for value in loginErrors.values():
            messages.error(request, value)
        return redirect('/')
    else: 
        usersWithEmail = User.objects.filter(email= request.POST['email'])
        request.session['uuid'] = usersWithEmail[0].id
        return redirect('/dashboard')
    
def logout(request):
    request.session.clear()
    return redirect('/')

###############################################################################

def add_form(request):
    context = {
        'loggedInUser': User.objects.get(id = request.session['uuid']),
    }
    return render(request, "add_wish.html", context)

def make_wish(request):
    errors= Item.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        Item.objects.create(item = request.POST['item'], desc = request.POST['desc'], wisher = User.objects.get(id = request.session['uuid']))
    return redirect('/dashboard')
    
def edit_form(request, num):

    context= {
        'all_wishes': Item.objects.get(id=num),
        'loggedInUser': User.objects.get(id = request.session['uuid']),
        }
    return render(request, "edit_wish.html", context)

def edit_wish(request, num):
    errors= Item.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit_form/edit/'+str(num))
    else:
        editwish = Item.objects.get(id=num)
        if request.POST['item']:
            editwish.item = request.POST['item']
        
        if request.POST['desc']:
            editwish.desc = request.POST['desc']
        editwish.save()
    return redirect('/dashboard')


def remove(request, num):
    Item.objects.get(id=num).delete()
    return redirect('/dashboard')

#0000000000000000000000000000000000000000000
def grant_wish(request, num):
    wish_granted = Item.objects.get(id=num)
    wish_granted.date_granted = wish_granted.updated_at
    wish_granted.save()
    
    return redirect("/dashboard")


def like_wish(request, num):
    wish = Item.objects.get(id=num)
    user = User.objects.get(id = request.session['uuid'])
    wish.likes.add(user)
    return redirect("/dashboard")
def unlike_wish(request, num):
    wish = Item.objects.get(id=num)
    user = User.objects.get(id = request.session['uuid'])
    wish.likes.remove(user)
    return redirect("/dashboard")

def wishes_stats(request):
    all_granted = Item.objects.exclude(date_granted = None)
    user_wishes = Item.objects.filter(wisher = request.session['uuid'])
    user_granted = user_wishes.exclude(date_granted = None)
    not_granted = user_wishes.filter(date_granted = None)

    context = {
        'all_granted_wishes': all_granted,
        'user_granted_wishes': user_granted, 
        'not_granted': not_granted,
        'loggedInUser': User.objects.get(id = request.session['uuid']),

    }

    return render(request, 'wishes_stats.html', context)