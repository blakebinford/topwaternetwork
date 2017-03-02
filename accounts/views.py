from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from posts.models import FishingReport
from subnetwork.models import SubNetwork
from django.core.mail import send_mail
# Create your views here.


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html',
                              {'error': 'Username has already been taken.'})

            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password'],
                                                email=request.POST['email'],
                                                first_name=request.POST['firstname'],
                                                last_name=request.POST['lastname'],
                                                )
                profile = UserProfile()
                profile.user_relation = user
                profile.save()
                email_body = "Thank you for signing up with Top Water Network, {}. Connect with fishing " \
                             "guides and find fishing reports of your favorite fishing spots.".format(user.username)
                send_mail('Thank you for signing up with Top Water Network!', email_body, 'noreply@topwaternetwork.com',
                          [user.email], fail_silently=False)

                login(request, user)
            return redirect('subnetworks:all_subs')
        else:
            return render(request, 'accounts/signup.html',
                          {'error': 'Passwords Didn\'t match'})
    else:
        return render(request, 'accounts/signup.html')


def guide_signup(request):
    subnetwork = SubNetwork.objects.all()
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html',
                              {'error': 'Username has already been taken.'})

            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password'],
                                                email=request.POST['email'],
                                                first_name=request.POST['firstname'],
                                                last_name=request.POST['lastname'],
                                                )
                profile = UserProfile()
                profile.user_relation = user
                profile.fish_location = request.POST['sub']
                profile.user_bio = request.POST['user_bio']
                profile.phone_number = request.POST['phone']
                profile.is_guide = True
                profile.save()
                login(request, user)
            return redirect('subnetworks:all_subs')
        else:
            return render(request, 'accounts/guide_signup.html',
                          {'error': 'Passwords Didn\'t match', })
    else:
        return render(request, 'accounts/guide_signup.html', {'subnetwork': subnetwork})


def loginview(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST["next"])
            return redirect('/accounts/{}'.format(user.id),
                            {'error': 'Log in successful.'})

        else:
            return render(request, 'accounts/login.html',
                          {'error': 'The username or password are incorrect.'})

    else:
        return render(request, 'accounts/login.html')


def user_detail(request, user):
    user_check = User.objects.get(id=user)
    if user_check.userprofile.is_guide:
        user_posts = FishingReport.objects.filter(author=user).order_by('-pub_date')
        user_page = User.objects.get(id=user)
        return render(request, 'accounts/guide_detail.html', {'user_posts': user_posts,
                                                              'user_page': user_page})
    else:
        user_posts = FishingReport.objects.filter(author=user).order_by('-pub_date')
        user_page = User.objects.get(id=user)
        return render(request, 'accounts/user_detail.html', {'user_posts': user_posts,
                                                             'user_page': user_page})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def all_user_subs(request, user):
    user_subs = SubNetwork.objects.filter(followers=user)
    return render(request, 'accounts/user_subs.html', {'user_subs': user_subs, })


def account_choose(request):
    return render(request, 'accounts/choose_account.html')
