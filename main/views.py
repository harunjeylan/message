from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import  UserFriend, Messages, Profile
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, updateProfileForm, updateUserForm, WriteUpdateMessageForm
from django.http import  JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

def loginPage(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
                
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('home')
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
    
	return render(request, 'main/login_register.html', context={'page': 'login_page', "form": form})



def logoutPage(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = RegisterForm()
    if request.method == 'POST':
        if request.POST.get('first_name') == '':
            messages.error(request, 'First name is requere!')
            return render(request, 'main/login_register.html', {'page': 'register_page'})

        if User.objects.filter(email=request.POST.get('email')).exists():
            messages.error(request, 'User is allredy exist!')
            return render(request, 'main/login_register.html', {'page': 'register_page'})
        else:
            if request.POST.get('password1') != request.POST.get('password2'):
                messages.error(request, 'password dase not matche!')
                return render(request, 'main/login_register.html', {'page': 'register_page'})
        new_user = RegisterForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            messages.success(request, "you have registerd please login.")
            return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            form = RegisterForm(request.POST)
    context = {'form': form, 'page': 'register_page'}
    return render(request, 'main/login_register.html', context)


@login_required(login_url='/login')
def home(request):
    sender = User.objects.get(username=request.user.username)
    if request.GET.get('serche-friends') != '' and bool(request.GET.get('serche-friends')):
        friends = User.objects.filter(
            Q(first_name__icontains=request.GET.get('serche-friends')) |
            Q(last_name__icontains=request.GET.get('serche-friends')) |
            Q(username__icontains=request.GET.get('serche-friends')) |
            Q(email__icontains=request.GET.get('serche-friends'))
        )
        friend_info = []
        for frien in friends:
            
            get_friend = UserFriend.objects.filter(Q(user=sender) & Q(
                friends=frien) | Q(user=frien) & Q(friends=sender))
            if bool(get_friend):
                ms = get_friend.first().messages_set.all()
            else:
                ms = []
            ind = 0
            mess_length = len(ms)
            if mess_length > 0:
                ind = len(ms)-1
                friend_info.append(
                    {'obj': frien,  'mes': ms[ind], 'mess_length': mess_length})
            else:
                friend_info.append(
                    {'obj': frien,  'mes': ms, 'mess_length': mess_length})
    else:
        friends = UserFriend.objects.filter(Q(user=sender) | Q(friends=sender))
        friend_info = []
        for fr in friends:
            ms = fr.messages_set.all()
            ind = 0
            mess_length = len(ms)
            if mess_length > 0:
                ind = len(ms)-1
                friend_info.append(
                    {'obj': fr,  'mes': ms[ind], 'mess_length': mess_length})
            else:
                friend_info.append(
                    {'obj': fr,  'mes': ms, 'mess_length': mess_length})

    friend_info.reverse()
    context = {'friend_info': friend_info, 'page': 'home'}
    return render(request, 'main/home.html', context)


@login_required(login_url='/login')
def message(request, pk):
    sender = User.objects.get(username=request.user.username)
    friend = User.objects.get(username=pk)
    form = WriteUpdateMessageForm()
    if request.GET.get('serche-friends') != '' and bool(request.GET.get('serche-friends')):
        friends = User.objects.filter(
            Q(first_name__icontains=request.GET.get('serche-friends')) |
            Q(last_name__icontains=request.GET.get('serche-friends')) |
            Q(username__icontains=request.GET.get('serche-friends')) |
            Q(email__icontains=request.GET.get('serche-friends'))
        )
        friend_info = []
        for frien in friends:
            get_friend = UserFriend.objects.filter(Q(user=sender) & Q(
                friends=frien) | Q(user=frien) & Q(friends=sender))
            if bool(get_friend):
                ms = get_friend.first().messages_set.all()
            else:
                ms = []
            ind = 0
            mess_length = len(ms)
            if mess_length > 0:
                ind = len(ms)-1
                friend_info.append(
                    {'obj': frien,  'mes': ms[ind], 'mess_length': mess_length})
            else:
                friend_info.append(
                    {'obj': frien,  'mes': ms, 'mess_length': mess_length})
    else:
        friends = UserFriend.objects.filter(
            Q(user=sender) | Q(friends=sender))
        friend_info = []
        for fr in friends:
            ms = fr.messages_set.all()
            ind = 0
            mess_length = len(ms)
            if mess_length > 0:
                ind = len(ms)-1
                friend_info.append(
                    {'obj': fr,  'mes': ms[ind], 'mess_length': mess_length})
            else:
                friend_info.append(
                    {'obj': fr,  'mes': ms, 'mess_length': mess_length})

    # friend_info.reverse()
    context = {
        'reciever': friend,
        'form': form,
        'page': 'message',
        'friend_info': friend_info,
    }

    return render(request, 'main/home.html', context)


def upload_file(request):
    file = request.FILES.get("file")

    fss = FileSystemStorage()
    filename = fss.save(file.name, file)
    url = fss.url(filename)
    data = ContentFile(base64.b64decode(file), name=file.name)
    Messages.objects.create(doc=data)
    return JsonResponse({"link": data})


def getMessages(request, pk):
    sender = User.objects.get(username=request.user.username)
    friend = User.objects.get(username=pk)
    context = {}
    try:
        bitween = UserFriend.objects.get(Q(user=sender) & Q(
            friends=friend) | Q(user=friend) & Q(friends=sender))
    except:
        UserFriend.objects.create(user=request.user, friends=friend)
        bitween = UserFriend.objects.get(Q(user=sender) & Q(
            friends=friend) | Q(user=friend) & Q(friends=sender))

    if request.method == "POST":
        if request.POST.get('deleteMessage') == "true":
            message = Messages.objects.get(
                id=request.POST.get('messageId'))
            message.delete()
        elif request.POST.get('updateMessage') == "true":
            message = Messages.objects.get(
                id=request.POST.get('messageId'))
            if request.POST.get('text'):
                message.text = request.POST.get('text')
            if request.FILES.get('image'):
                message.image = request.FILES.get('image')
            if request.FILES.get('file'):
                message.file = request.FILES.get('file')
            message.save()
        else:
            Messages.objects.create(sender=sender, bitween=bitween, text=request.POST.get('text'),
                                    image=request.FILES.get('image'), file=request.FILES.get('file'))
    messages = bitween.messages_set.all()
    context["messages"] = list(messages.values())
    return JsonResponse(context)


@login_required(login_url='/login')
def update_message(request, f_pk, m_pk):
    message = Messages.objects.get(id=m_pk)
    sender = User.objects.get(username=request.user.username)
    friend = User.objects.get(username=f_pk)
    bitween = UserFriend.objects.get(Q(user=sender) & Q(
        friends=friend) | Q(user=friend) & Q(friends=sender))
    if request.method == 'POST' and bool(request.POST.get('text')):
        message.text = request.POST.get('text')
        message.save()
        return redirect('message', f_pk)
    messages = bitween.messages_set.all()
    context = {'messages': messages,
               'reciever': friend,
               'len_messages': len(messages),
               }
    return render(request, 'main/home.html', context)


@login_required(login_url='/login')
def profile(request, pk):
    user = User.objects.get(username=pk)
    profile = User.objects.get(username=pk).profile
    context = {"user":[{
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        "bio": profile.bio,
        "nickname": profile.nickname,
        "avater": profile.avater.url
        }]}
    return JsonResponse(context)


@login_required(login_url='/login')
def updateProfile(request):
    if request.method == 'POST':
        p_form = updateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = updateUserForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, "profile is saved")
            return redirect('home')
        else:
            messages.error(request, "profile is not saved")

    p_form = updateProfileForm(instance=request.user.profile)
    u_form = updateUserForm(instance=request.user)
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'main/updateProfile.html', context)


@login_required(login_url='/login')
def add_friends(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            friend = User.objects.get(username=username)
        except:
            try:
                friend = User.objects.get(username=username)
            except:
                messages.error(request, 'user is not join yet!')
                return render(request, 'main/add_friends.html')

        userFruend = UserFriend.objects.filter(Q(user=request.user) & Q(
            friends=friend) | Q(user=friend) & Q(friends=request.user))

        if not bool(userFruend):
            UserFriend.objects.create(user=request.user, friends=friend)
            return redirect('home')
        else:
            messages.error(request, 'user is alrady your friends')
    context = {}
    return render(request, 'main/add_friends.html', context)


@login_required(login_url='/login')
def deleteFriend(request, pk):
    sender = User.objects.get(username=request.user.username)
    friend = User.objects.get(username=pk)
    bitween = UserFriend.objects.get(Q(user=sender) & Q(
        friends=friend) | Q(user=friend) & Q(friends=sender))
    bitween.delete()
    return redirect('home')