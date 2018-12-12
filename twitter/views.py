from twitter.forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.shortcuts import reverse, render, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout


def signup_view(request):

    html = 'signup.html'

    form = SignupForm(None or request.POST)

    if form.is_valid():
        print('FORM VALID')
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password']
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


def home_view(request):
    return render(request, 'homepage.html')