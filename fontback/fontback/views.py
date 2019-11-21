from __future__ import unicode_literals
from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect,Http404
from django.contrib import auth
from django.contrib.auth.models import User
from main_move.models import MainMovie
from django.views.decorators.csrf import csrf_exempt


def index(req):
    user_id = ''
    movie_all = MainMovie.objects.all()
    movie = movie_all[0:6]
    movie_date = MainMovie.objects.order_by('-release_date')[0:6]
    movie_rating = MainMovie.objects.order_by('-rating')[0:6]
    movie_added = movie_all[0:6]
    return render(req, 'index.html', {'movies': movie, 'user_id': user_id, 'movie_dates': movie_date, 'movie_ratings': movie_rating, 'movie_addeds': movie_added})


def moves_list(req):
    return render(req, 'moves_list.html')

