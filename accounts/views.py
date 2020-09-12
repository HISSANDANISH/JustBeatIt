from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from . models import Profile, FriendRequest
import random
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


def users_list(request):
	users = Profile.objects.exclude(user=request.user)
	sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
	sent_to = []
	friends = []
	for user in users:
		friend = user.friends.all()
		for f in friend:
			if f in friends:
				friend = friend.exclude(user=f.user)
		friends+=friend
	my_friends = request.user.profile.friends.all()
	for i in my_friends:
		if i in friends:
			friends.remove(i)
	if request.user.profile in friends:
		friends.remove(request.user.profile)
	random_list = random.sample(list(users), min(len(list(users)), 10))
	for r in random_list:
		if r in friends:
			random_list.remove(r)
	friends+=random_list
	for i in my_friends:
		if i in friends:
			friends.remove(i)
	for se in sent_friend_requests:
		sent_to.append(se.to_user)
	context = {
		'users': friends,
		'sent': sent_to
	}
	return render(request, "users_list.html", context)


def friend_list(request):
	p = request.user.profile
	friends = p.friends.all()
	context={
	'friends': friends
	}
	return render(request, "friend_list.html", context)









def send_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest, created = FriendRequest.objects.get_or_create(
			from_user=request.user,
			to_user=user)
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))


def cancel_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(
			from_user=request.user,
			to_user=user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))


def accept_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))


def delete_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

def delete_friend(request, id):
	user_profile = request.user.profile
	friend_profile = get_object_or_404(Profile, id=id)
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)
	return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))


def profile_view(request, slug):
	p = Profile.objects.filter(slug=slug).first()
	u = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
	user_posts = Post.objects.filter(user_name=u)

	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user).filter(to_user=p.user)) == 1:
				button_status = 'friend_request_sent'

	context = {
		'u': u,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
		'post_count': user_posts.count
	}

	return render(request, "users/profile.html", context)


def edit_profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('my_profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context ={
		'u_form': u_form,
		'p_form': p_form,
	}
	return render(request, 'users/edit_profile.html', context)

def my_profile(request):
	p = request.user.profile
	you = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=you)
	rec_friend_requests = FriendRequest.objects.filter(to_user=you)
	user_posts = Post.objects.filter(user_name=you)
	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user).filter(to_user=you)) == 1:
				button_status = 'friend_request_sent'

	context = {
		'u': you,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
		'post_count': user_posts.count
	}

	return render(request, "users/profile.html", context)


def search_users(request):
	query = request.GET.get('q')
	object_list = User.objects.filter(username__icontains=query)
	context ={
		'users': object_list
	}
	return render(request, "users/search_users.html", context)