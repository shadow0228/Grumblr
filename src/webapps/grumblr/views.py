from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist 
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.core import serializers
from django.core.mail import EmailMultiAlternatives

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from grumblr.models import *
from grumblr.form import *
import json
from django.core.serializers.json import DjangoJSONEncoder


@login_required

def home(request):
    posts = Post.objects.all().order_by('-created')

    for post in posts:
        comments = Comment.objects.filter(post=post).order_by('-created')
        post.comments = comments

    context = {'posts' : posts}
    return render(request, 'grumblr/GlobalStream.html', context)

def forgetPassword(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'grumblr/ForgetPassword.html', context)

    if not User.objects.filter(username=request.POST['username']).exists():
        errors = ['Can not find this user']
        context = {'errors':errors}
        return render(request, 'grumblr/ForgetPassword.html', context)

    user = User.objects.get(username=request.POST['username'])
    send_reset_email(str(user.id) ,user.email)
    context = {}
    return redirect(home)


@login_required
def follow(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(owner=user)
    follows = profile.follows.all()
    posts = Post.objects.filter(user__in=follows).order_by('-created')

    context = {'posts' : posts, 'follows':follows}
    return render(request, 'grumblr/FollowerStream.html', context)

@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(user=user).order_by('-created')
    profile = Profile.objects.get(owner=user)
    context = {'posts': posts, 'user': user, 'profile':profile}

    return render(request, 'grumblr/Profile.html', context)

@login_required
def profileEdit(request, id):

    errors = []

    user = User.objects.get(id=id)
    profile = Profile.objects.get(owner=user)
    posts = Post.objects.filter(user=user).order_by('-created')
    if request.method == 'GET':
        context = {'profile':profile, 'user': user}
        return render(request, 'grumblr/ProfileEdit.html', context)

    user.first_name = request.POST['firstname']
    user.last_name = request.POST['lastname']
    profile.age = request.POST['age']
    profile.bio = request.POST['bio']

    if 'password1' in request.POST and request.POST['password1']:
        if not 'password2' in request.POST or not request.POST['password2']:
            errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if errors:
        context = {'profile':profile, 'user': user, 'errors': errors}
        return render(request, 'grumblr/ProfileEdit.html', context)

    if 'password1' in request.POST and request.POST['password1']:
        user.set_password(request.POST['password1'])
    form = ImageUploadForm(request.POST, request.FILES)

    if form.is_valid():
        profile.image = request.FILES['image']

    user.save()
    profile.save()

    context = {'posts': posts, 'user': user, 'profile':profile}
    return render(request, 'grumblr/Profile.html', context)

@login_required
def add_post(request):
    # Creates a new item if it is present as a parameter in the request


    new_item = Post(text=request.POST['post_content'], user=request.user)
    new_item.save()

    return redirect(home)

def add_comment(request):
    if request.method == 'POST':
        if 'text' in request.POST:
            post = Post.objects.get(id=request.POST['post'])
            new_comment = Comment(text=request.POST['text'], post=post, owner=request.user)
            new_comment.save()
            
            posts = Post.objects.all().order_by('-created')
            for post in posts:
                comments = Comment.objects.filter(post=post).order_by('-created')
                post.comments = comments

            context = {'posts' : posts}
            return render(request, 'grumblr/GlobalStream.html', context)

    
def addfollow(request, id1, id2):
    # Creates a new item if it is present as a parameter in the request

    user = User.objects.get(id=id1)
    follower = User.objects.get(id=id2)
    profile = Profile.objects.get(owner=user)
    profile.follows.add(follower)
    profile = Profile.objects.get(owner=follower)
    posts = Post.objects.filter(user=follower).order_by('-created')
    context = {'posts': posts, 'user': follower, 'profile':profile}
    return render(request, 'grumblr/Profile.html', context)

def deletefollow(request, id1, id2):
    # Creates a new item if it is present as a parameter in the request

    user = User.objects.get(id=id1)
    follower = User.objects.get(id=id2)
    profile = Profile.objects.get(owner=user)
    profile.follows.remove(follower)
    profile = Profile.objects.get(owner=follower)
    posts = Post.objects.filter(user=follower).order_by('-created')
    context = {'posts': posts, 'user': follower, 'profile':profile}
    return render(request, 'grumblr/Profile.html', context)

def send_email(id, email):
    subject = "Grumblr Sign In"
    from_email, to = settings.EMAIL_HOST_USER, email
    text_content = 'Text'
    html_content = '<a href="http://ec2-35-161-10-240.us-west-2.compute.amazonaws.com/confirm/' + id + '">Click</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_reset_email(id, email):
    subject = "Grumblr reset email"
    from_email, to = settings.EMAIL_HOST_USER, email
    text_content = 'Reset email'
    html_content = '<a href="http://ec2-35-161-10-240.us-west-2.compute.amazonaws.com/changePassword/' + id + '">Reset you password</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def confirm(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect(home)

def changePassword(request, id):

    action = '/changePassword/' + str(id) + '/'
    context = {'action':action}

    if request.method == 'GET':
        context['form'] = ChangePasswordForm()
        return render(request, 'grumblr/ChangePassword.html', context)

    form = ChangePasswordForm(request.POST)
    context['form'] = form

    if form.is_valid():
        user = User.objects.get(id=id)
        user.set_password(request.POST['password1'])
        user.save()
        return redirect(home)
    
    return render(request, 'grumblr/ChangePassword.html', context)

def register(request):

    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'grumblr/SignUp.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'grumblr/SignUp.html', context)

   
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password1'], \
                                        first_name=request.POST['firstname'], \
                                        last_name=request.POST['lastname'], \
                                        email=request.POST['email'] )

    new_user.is_active = False
    new_user.save()

    new_user_profile = Profile(owner=new_user)
    new_user_profile.save()

    send_email( str(new_user.id) ,new_user.email)

    return redirect(home)

def get_post(request):
    bigDic = []
    posts = Post.objects.all().order_by('-created')

    for post in posts:   
        dic = {}
        dic['postText'] = post.text
        dic['image'] = str(post.user.profile.image.url)
        dic['userId']= post.user.id
        dic['user'] = post.user.username
        dic['create'] = post.created.strftime('%b. %d, %Y, %H:%M')
        dic['postId'] = post.id

        bigDic.append(dic)

    return HttpResponse(json.dumps(bigDic, cls=DjangoJSONEncoder), content_type="application/json")

def get_comment(request):

    bigDic = []

    posts = Post.objects.all().order_by('-created')
    for post in posts:
        comDic = []
        comments = Comment.objects.filter(post=post).order_by('-created')

        for comment in comments:
            dic = {}
            dic['image'] = str(comment.owner.profile.image.url)
            dic['userId']= comment.owner.id
            dic['user'] = comment.owner.username
            dic['create'] = comment.created.strftime('%b. %d, %Y, %H:%M')
            dic['commentText'] = comment.text

            comDic.append(dic)
        bigDic.append(comDic)

    return HttpResponse(json.dumps(bigDic, cls=DjangoJSONEncoder), content_type="application/json")

# # Create your views here.
