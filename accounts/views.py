from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from . models import Profile
# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name'] 
        last_name = request.POST['last_name'] 
        username = request.POST['username']
        email = request.POST['email'] 
        password = request.POST['pass'] 
        re_password = request.POST['re_pass'] 
        if password==re_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Emails already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, password=password,email=email,last_name=last_name,username=username)
                subject = 'Thank you for registering to JustBeatIt'
                message = 'Hello '+first_name+' Start rocking by connecting with like-minded musicians '
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail( subject, message, email_from, recipient_list)
                user.save()
                profile = Profile(user=user)
                if profile is not None:
                    print('Profile should be created')
                profile.save()
                auth.login(request, user)
                return redirect('home')
        else:
            messages.info(request, "Password did not Match")
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user_name = user.username
            user = auth.authenticate(username=user_name,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid Password')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Email')  
            return redirect('login')              
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def email(request):
    subject = 'Thank you for registering to our site'
    message = 'It means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email]
    send_mail( subject, message, email_from, recipient_list)

    return redirect('/')

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('/')