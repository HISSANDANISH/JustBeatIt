from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from . models import Profile, FriendRequest
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def register1(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You can now login!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form':form})

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
                profile.save()
                auth.login(request, user)
                return redirect('my_profile')
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
                return redirect("my_profile")
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
        return redirect('my_profile')
    else:
        return redirect('/')

@login_required
def users_list(request):
	instruments_choices=request.user.profile._meta.get_field('instruments').choices
	music_choices=request.user.profile._meta.get_field('like_music').choices 
	if ((request.GET.get('usearch') is not None) and (request.GET.get('usearch') != '')):
		query = request.GET.get('usearch')
		user_list = User.objects.filter(username__icontains=query)
		profile_list = []
		sent_to = []
		sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
		for se in sent_friend_requests:
			sent_to.append(se.to_user.profile)
		friend_list = request.user.profile.friends.all()
		if (request.GET.get('instrument') is not None) and (request.GET.get('instrument') != "None") and (request.GET.get('music') is not None) and (request.GET.get('music') != "None") :
			for user in user_list:
				if (user.profile.instruments == request.GET.get('instrument')) and (user.profile.like_music == request.GET.get('music')):
					profile_list.append(user.profile)
			selected_instrument = request.GET.get('instrument')
			selected_music = request.GET.get('music')
		elif (request.GET.get('instrument') is not None) and (request.GET.get('instrument') != "None"):
			for user in user_list:
				if (user.profile.instruments == request.GET.get('instrument')):
					profile_list.append(user.profile)
			selected_instrument = request.GET.get('instrument')
			selected_music = "None"
		elif (request.GET.get('music') is not None) and (request.GET.get('music') != "None"):		
			for user in user_list:
				if (user.profile.like_music == request.GET.get('music')):
					profile_list.append(user.profile)
			selected_instrument = "None"
			selected_music = request.GET.get('music')
		else:
			for user in user_list:
				profile_list.append(user.profile)
			selected_music = "None"
			selected_instrument = "None"
		context={
			'users':profile_list,
			'usearch':query,
			'request_user_friends':friend_list,
			'request_user':request.user.profile,
			'sent': sent_to,
			'instruments_choices': instruments_choices,
			'music_choices': music_choices,
			'selected_instrument' : selected_instrument,
			'selected_music' : selected_music,
		}
	else:
		user_list = Profile.objects.exclude(user=request.user)
		sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
		sent_to = []
		profile_list = []
		for se in sent_friend_requests:
			sent_to.append(se.to_user.profile)
		friend_list = request.user.profile.friends.all()
		if (request.GET.get('instrument') is not None) and (request.GET.get('instrument') != "None") and (request.GET.get('music') is not None) and (request.GET.get('music') != "None") :
			for user in user_list:
				if (user.instruments == request.GET.get('instrument')) and (user.like_music == request.GET.get('music')):
					profile_list.append(user)
			selected_instrument = request.GET.get('instrument')
			selected_music = request.GET.get('music')
		elif (request.GET.get('instrument') is not None) and (request.GET.get('instrument') != "None"):
			for user in user_list:
				if (user.instruments == request.GET.get('instrument')):
					profile_list.append(user)
			selected_instrument = request.GET.get('instrument')
			selected_music = "None"
		elif (request.GET.get('music') is not None) and (request.GET.get('music') != "None"):		
			for user in user_list:
				if (user.like_music == request.GET.get('music')):
					profile_list.append(user)
			selected_instrument = "None"
			selected_music = request.GET.get('music')
		else:
			selected_music = "None"
			selected_instrument = "None"
			friends = []
			for user in user_list:
				friend = user.friends.all()
				for f in friend:
					if f in friends:
						friend = friend.exclude(user=f.user)
				friends+=friend
			my_friends = request.user.profile.friends.all()
			for i in my_friends:
				if i in friend:
					friends.remove(i)
			if request.user.profile in friends:
				friends.remove(request.user.profile)
			profile_list = friends
		context = {
			'users': profile_list,
			'sent': sent_to,
			'request_user_friends' :friend_list,
			'instruments_choices': instruments_choices,
			'music_choices': music_choices,
			'selected_instrument' : selected_instrument,
			'selected_music' : selected_music,
		}
	return render(request, "users_list.html", context)

@login_required
def friend_list(request):
	p = request.user.profile
	friends = p.friends.all()
	context={
	'friends': friends
	}
	return render(request, "friend_list.html", context)

@login_required
def request_list(request):
	request_list = FriendRequest.objects.filter(to_user=request.user)
	context ={
		'request_list' : request_list
	}
	return render(request, 'request_list.html', context)

@login_required
def send_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	friend_request , created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=user)
	subject = request.user.username + "has sent you Invitation "
	message = "Hi "+ user.username+" , Accept invitation and start making amazing music ! From, JustBeatIt"
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [user.email]
	send_mail( subject, message, email_from, recipient_list)
	return redirect('users_list')


@login_required
def cancel_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.get(
			from_user=request.user,
			to_user=user)
	frequest.delete()
	return redirect('my_profile')

@login_required
def accept_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.get(from_user=from_user, to_user=request.user)
	user1 = request.user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	frequest.delete()
	subject = request.user.username + " accepted your Invitation "
	message = "Enjoy your connection and make amazing music!!"
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [from_user.email]
	send_mail( subject, message, email_from, recipient_list)
	return redirect('my_profile')

@login_required
def delete_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

@login_required
def delete_friend(request, id):
	user_profile = request.user.profile
	friend_profile = get_object_or_404(Profile, id=id)
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)
	return redirect('friend_list')

@login_required
def profile_view(request, slug):
	p = Profile.objects.get(slug=slug)
	u = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_connection'
		# if we have sent him a friend request
	if FriendRequest.objects.filter(from_user=request.user,to_user=p.user):
		button_status = 'request_sent'
	# send email
	subject = request.user.username + " has Viewed Your Profile "
	message = "Invite Or Connect with musicians by logging in Now!!"
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [p.user.email]
	send_mail( subject, message, email_from, recipient_list)
	context = {
		'u': u,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
	}

	return render(request, "profile.html", context)

@login_required
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
	return render(request, 'edit_profile.html', context)

@login_required
def edit_music(request):
	if request.method == 'POST':
		if request.POST.get('instrument_add', default=None):
			request.user.profile.instruments.append(request.POST.get('instrument_add'))
			request.user.profile.save()
			return redirect('edit_music')
		elif request.POST.get('music_add', default=None):
			request.user.profile.like_music.append(request.POST.get('music_add'))
			request.user.profile.save()
			return redirect('edit_music')
		elif request.POST.get('delete_instrument', default=None):
			request.user.profile.instruments.remove(request.POST.get('delete_instrument'))
			request.user.profile.save()
			return redirect('edit_music')
		elif request.POST.get('delete_music', default=None):
			request.user.profile.like_music.remove(request.POST.get('delete_music'))
			request.user.profile.save()
			return redirect('edit_music')
		else:
			return redirect('my_profile')
	else:
		context ={
			'instruments' : request.user.profile.instruments,
			'music' : request.user.profile.like_music
		}
		return render(request, 'edit_music.html', context)

@login_required
def my_profile(request):
	p = request.user.profile
	you = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=you)
	rec_friend_requests = FriendRequest.objects.filter(to_user=you)
	#user_posts = Post.objects.filter(user_name=you)
	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_connection'

		# if we have sent him a friend request
	context = {
		'u': you,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
		#'post_count': user_posts.count
	}

	return render(request, "profile.html", context)

@login_required
def search_users(request):
	if query is None:
		return redirect('users_list')
	else:
		user_list = User.objects.filter(username__icontains=query)
		profile_list = []
		for user in user_list:
			profile_list +=[user.profile]
		context={
			'users':profile_list,
			'usearch':query
		}
		print(user_list)
	return render(request, "users_list.html", context)