from twitter.forms import SignupForm, LoginForm, AddTweet
from twitter.models import Tweet, TwitterUser
from django.contrib.auth.models import User
from django.shortcuts import reverse, render, HttpResponseRedirect, redirect
from django.contrib.auth import login, authenticate, logout
import datetime


def signup_view(request):

    html = 'signup.html'

    form = SignupForm(None or request.POST)

    if form.is_valid():
        
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password']
        )
        
        twitter_user = TwitterUser.objects.create(
            username=data['username'],
            user=user,
        )
        # print(user)
        login(request, user)
        # login(request, twitter_user)

        return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})

def login_view(request):
    html = 'login.html'

    form = LoginForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def home_view(request):
    twitter_users = TwitterUser.objects.all()
    logged_in_user = TwitterUser.objects.filter(username=request.user).first()
    following_list = []
    username_following_list = []

    for x in logged_in_user.following.all():
        following_list.append(x.id)
    # print(following_list)

    for x in twitter_users:
        if x.id in following_list:
            # print(x)
            username_following_list.append(x)
        

    results = Tweet.objects.all()
    final_results = []

    for x in results:
        if x.twitter_user in username_following_list:
            print(x.twitter_user)
            print(x.body)
            final_results.append(x)

    print(final_results)
    is_logged_in = request.user.is_authenticated
    
    if is_logged_in:
        return render(request, 'homepage.html', {'data': final_results})
    else:
        return redirect('login/', permananent=False)

def individual_tweet_view(request, tweet_pk):
    filtered_result = Tweet.objects.all().filter(id=tweet_pk)[0]
    return render(request, 'individual_tweet.html', {'data': filtered_result})

def user_profile_view(request, user):

    logged_in_user = TwitterUser.objects.filter(username=request.user).first()
    print(logged_in_user)

    if request.method == 'POST':
        print(request.POST['user_id'])
        targeted_user = TwitterUser.objects.filter(id=request.POST['user_id']).first()
        print(targeted_user)
        logged_in_user.following.add(targeted_user)
        print(logged_in_user.following.all())
    


    filtered_result = TwitterUser.objects.all().filter(username=user).first()
    filtered_tweets = Tweet.objects.all().filter(twitter_user=filtered_result)
    
    return render(request, 'user_profile.html', {'user': filtered_result,
                                                 'tweets': filtered_tweets})

def compose_view(request):
    html = 'compose.html'
    form = AddTweet(None or request.POST)
    print(request.user.id)
    # print(TwitterUser.objects.all())
    # print(User.objects.all())
    # for x in TwitterUser.objects.all():
        # print(x.id)
        # print (x.username)
        
    x = datetime.datetime.now()

    if form.is_valid():
        data = form.cleaned_data
        tweet = Tweet.objects.create(
            body=data['body'],
            twitter_user=TwitterUser.objects.filter(id=request.user.id).first(),
            date_time=x.strftime("%b") + " " + str(x.day) + ", " + str(x.year) + ", " + str(x.strftime("%I")) + ":" + str(x.strftime("%M")) + " " + x.strftime("%p")
        )
        return render(request, 'success.html')
    else:
        print(TwitterUser.objects.all())

    return render(request, html, {'form': form})
