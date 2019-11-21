"""fontback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from main_move import main_move_views
from account import account_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),

    url(r'^login', account_views.account_login),

    url(r'^register', account_views.register),

    url(r'^logout', account_views.logout),

    url(r'^user_profile_display', account_views.user_profile_display),

    url(r'^user_profile_edit',
    account_views.user_profile_edit),

    url(r'^moves_list/(\S*)', main_move_views.moves_list_type),
    url(r'^search_list/(\S*)', main_move_views.search_list),
    url(r'^single/(\S*)', main_move_views.single),

    url(r'^userbased_recommend', main_move_views.userbased_recommend)
    # url(r'^xt_user_based_recommend', main_move_views.xt_user_based_recommend)
]
