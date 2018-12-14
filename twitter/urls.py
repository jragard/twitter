"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from twitter.views import home_view, signup_view, login_view, compose_view, logout_view, individual_tweet_view, user_profile_view
from twitter.models import TwitterUser, Tweet
from django.contrib.auth.models import User

admin.site.register(TwitterUser)
admin.site.register(Tweet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='homepage'),
    path('signup/', signup_view),
    path('login/', login_view),
    path('compose/', compose_view),
    path('logout/', logout_view),
    path('<int:tweet_pk>', individual_tweet_view),
    path('<slug:user>', user_profile_view),
]
