from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from main_move.models import MainMovie
from main_move.search_movie_post import SearchForm
from django.db.models import Q
from account.models import UserAndMovie
# from main_move import Recommend
import operator
import json
# from .models import Happy
# sc = Recommend.CreateSparkContext()
# #print("==========数据准备===============")
# Recommend.PrepareData(sc)
# Recommend.PrepareData2(sc)
# #print("==========载入模型===============")
# model = Recommend.loadModel(sc)
def type_trans(kind):
    temp = 0
    if kind == 'action':
        temp = '动作'
    if kind == 'plot':
        temp =  '剧情'
    if kind == 'science':
        temp =  '科幻'
    if kind == 'strange':
        temp =  '悬疑'
    if kind == 'disaster':
        temp =  '灾难'
    if kind == 'thriller':
        temp =  '惊悚'
    if kind == 'terror':
        temp =  '恐怖'
    if kind == 'crime':
        temp =  '犯罪'
    if kind == 'homo':
        temp =  '同性'
    if kind == 'music':
        temp =  '音乐'
    if kind == 'dance':
        temp =  '歌舞'
    if kind == 'gongfu':
        temp =  '武侠'
    if kind == 'bio':
        temp =  '历史'
    if kind == 'war':
        temp =  '战争'
    if kind == 'west':
        temp =  '西部'
    if kind == 'fariy':
        temp =  '奇幻'
    if kind == 'adventure':
        temp =  '冒险'
    if kind == 'sexy':
        temp =  '情色'
    return temp

def area_trans(kind):
    if kind == 'china':
        temp = '中国大陆'
    if kind == 'hk':
        temp = '香港'
    if kind == 'taiwan':
        temp = '台湾'
    if kind == 'japan':
        temp = '日本'
    if kind == 'koera':
        temp = '韩国'
    if kind == 'india':
        temp = '印度'
    if kind == 'thailand':
        temp = '泰国'
    if kind == 'england':
        temp = '英国'
    if kind == 'france':
        temp = '法国'
    if kind == 'germany':
        temp = '德国'
    if kind == 'italy':
        temp = '意大利'
    if kind == 'iran':
        temp = '伊朗'
    if kind == 'australia':
        temp = '澳大利亚'
    if kind == 'sweden':
        temp = '瑞典'
    if kind == 'denmark':
        temp = '丹麦'
    if kind == 'spain':
        temp = '西班牙'
    if kind == 'russia':
        temp = '俄罗斯'
    if kind == 'canada':
        temp = '加拿大'
    if kind == 'ireland':
        temp = '爱尔兰'
    if kind == 'brazil':
        temp = '巴西'
    return temp

def moves_list_type(req, kind):
    # print(kind)
    # print(type(kind))
    ctx = dict()
    temp = type_trans(str(kind))
    if temp == 0:
        temp = area_trans(str(kind))
        ctx['move'] = MainMovie.objects.filter(regions__contains=temp)[0:30]
    else:
        ctx['move'] = MainMovie.objects.filter(types__contains=temp)[0:30]
    #print(temp)
    ctx['type'] = temp
    #print(ctx['move'])
    if not ctx['move']:
        return render(req, 'search_no_result.html')
    return render(req, 'moves_list.html', ctx)

def search_list(req, kind):

    ctx = dict()
    target = req.POST['Search']

    #print("testtest")
    #print(target)

    ctx['moves'] = MainMovie.objects.filter(
        Q(title__contains=target)
        |
        Q(actors__contains=target)
        |
        Q(types__contains=target)
    )[0:30]
    # ctx['search'] = target
    # ctx['test'] = req.
    if not ctx['moves']:
        return render(req, 'search_no_result.html')
    # print(ctx['moves'])
    return render(req, 'search_list.html', ctx)

def single(req,re1):

    ctx = dict()
    ctx['move'] = MainMovie.objects.get(herf=re1)
    target = UserAndMovie.objects.filter(user_id=req.user.id).values('movie_id')
    # print(target)
    if target:
        likes = []
        for ele in target:
            likes.append(ele['movie_id'])
        # print(type(target))
        res = commend(likes)
        print(res)
        if len(res) <= 6:
            ctx['like'] = MainMovie.objects.order_by('-score')[0:5]

        else:
            ctx['like'] = MainMovie.objects.filter(
                Q(herf=res[0])
                |
                Q(herf=res[1])
                |
                Q(herf=res[2])
                |
                Q(herf=res[3])
                |
                Q(herf=res[4])
                |
                Q(herf=res[5])
            )
        return render(req, 'single.html', ctx)
    else:
        return render(req, 'single.html', ctx)


    # res = commend(likes)
    return render(req, 'single.html', ctx)

def commend(x):

    if len(x) <= 6:
        return set(x)
    else:
        a = dict()
        for i in x:
            a[i] = x.count(i)
        a = sorted(a.items(), key= operator.itemgetter(1))
    commend_set = []
    for ele in a:
        # print(ele[0])
        commend_set += commend_set + findsimilar(ele[0])
    commend_set = set(commend_set)
    # print(commend_set)
    # print(x)
    temp = commend_set - (set(x) & commend_set)
    # print(temp)
    return list(temp)

def findsimilar(id):
    # print(id)
    # print(type(id))
    tar_type = MainMovie.objects.filter(herf=id).values('types')
    # print(tar_type[0]['types'])
    tar_actor = MainMovie.objects.filter(herf=id).values('actors')
    tar_title = MainMovie.objects.filter(herf=id).values('title')
    tar = MainMovie.objects.filter(title__contains=tar_type[0]['types']).filter(title__contains=tar_title[0]['title']).filter(actors__contains=tar_actor[0]['actors'],)
    if not tar:
        tar = MainMovie.objects.filter(
            Q(title__contains=tar_type[0]['types'])
            |
            Q(actors__contains=tar_actor[0]['actors'])
            |
            Q(title__contains=tar_title[0]['title'])
        ).values('herf')

    # print("ok")
    # print(tar)
    # print(type(tar))
    likes = []
    for ele in tar:
        # print(ele)
        likes.append(ele['herf'])
    # print(likes)
    return likes

def userbased_recommend(req):
    return render(req, 'userbased_recommend.html')
# def xt_user_based_recommend(req):
#     user_id = req.POST.get('user_id')
#     film_num = req.POST.get('film_nums')
#     type = 'USER'
#     # Username = request.session['username']
#     # User = models.UserProfile.objects.get(user=request.user)
#     UserId = user_id
#     # sc = Recommend.CreateSparkContext()
#     # id = input("对应id:")
#     num = film_num
#     #print("==========进行推荐===============")
#     if type == 'USER' or type == 'MOVIE':
#         movies = Recommend.recommend(model, type, UserId, num)
#     # dic_username = {'username': Username}
#     ctx = {}
#     ctx['movies'] = movies
#     ctx['user'] = UserId
#     # history = {}
#     ctx['info'] = Happy.objects.filter(user_id=UserId)
#
#     return render(req, 'userbased_recommend.html', ctx)