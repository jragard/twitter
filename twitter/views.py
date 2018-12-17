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
        
        TwitterUser.objects.create(
            username=data['username'],
            user=user,
        )
       
        login(request, user)

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


def notifications_view(request):
    logged_in_user = TwitterUser.objects.filter(username=request.user).first()
    results = Tweet.objects.all()

    notifications = []
    mention = '@' + logged_in_user.username
    notifications.clear()

    for tweet in results:
        if mention in tweet.body and tweet.viewed is False:
            tweet.viewed = True
            tweet.save()
            notifications.append(tweet)
            

    return render(request, 'notifications.html', {'notifications': notifications,
                                                  'notifications_length': len(notifications),})

    

def home_view(request):
    twitter_users = TwitterUser.objects.all()
    logged_in_user = TwitterUser.objects.filter(username=request.user).first()
    following_list = []
    username_following_list = []

    if logged_in_user is not None:
        for x in logged_in_user.following.all():
            following_list.append(x.id)

        for x in twitter_users:
            if x.id in following_list:
                username_following_list.append(x)

        results = Tweet.objects.all()

        notifications = []
        mention = '@' + logged_in_user.username
        notifications.clear()

        for tweet in results:
            if mention in tweet.body and tweet.viewed is False:
                notifications.append(tweet)
            

        final_results = []

        for x in results:
            if x.twitter_user in username_following_list or x.twitter_user == logged_in_user:
                final_results.append(x)

    is_logged_in = request.user.is_authenticated
    
    if is_logged_in:
        return render(request, 'homepage.html', {'data': reversed(final_results),
                                                 'notifications': notifications,
                                                 'notification_length': len(notifications),})
    else:
        return redirect('login/', permananent=False)


def individual_tweet_view(request, tweet_pk):
    filtered_result = Tweet.objects.all().filter(id=tweet_pk)[0]
    return render(request, 'individual_tweet.html', {'data': filtered_result})


def user_profile_view(request, user):

    logged_in_user = TwitterUser.objects.filter(username=request.user).first()
    logged_in_user_following = []

    if logged_in_user is not None:
        for x in logged_in_user.following.all():
            logged_in_user_following.append(x.username)
    
    if request.method == 'POST':
        targeted_user = TwitterUser.objects.filter(id=request.POST['user_id']).first()
        
        if str(targeted_user) not in logged_in_user_following:
            logged_in_user.following.add(targeted_user)
        else:
            logged_in_user.following.remove(targeted_user)
    
    filtered_result = TwitterUser.objects.all().filter(username=user).first()
    filtered_tweets = Tweet.objects.all().filter(twitter_user=filtered_result)

    target_user_following = []

    for x in filtered_result.following.all():
        target_user_following.append(x.username)
    
    return render(request, 'user_profile.html', {'user': filtered_result,
                                                 'user_string': str(filtered_result),
                                                 'tweets': filtered_tweets,
                                                 'logged_in_user': logged_in_user,
                                                 'following': logged_in_user_following,
                                                 'tweet_count': len(filtered_tweets),
                                                 'following_count': len(target_user_following),
                                                 'target_following': target_user_following,
                                                 })

def compose_view(request):
    html = 'compose.html'
    form = AddTweet(None or request.POST)
    
    x = datetime.datetime.now()

    if form.is_valid():
        data = form.cleaned_data
        Tweet.objects.create(
            body=data['body'],
            twitter_user=TwitterUser.objects.filter(id=request.user.id).first(),
            date_time=x.strftime("%b") + " " + str(x.day) + ", " + str(x.year) + ", " + str(x.strftime("%I")) + ":" + str(x.strftime("%M")) + " " + x.strftime("%p"),
            viewed=False
        )
        return render(request, 'success.html')
    else:
        print(TwitterUser.objects.all())

    return render(request, html, {'form': form})
