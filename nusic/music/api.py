from __future__ import unicode_literals
from .models import *
from restapi import api
from pprint import pprint
from django.forms.models import model_to_dict
from django.conf import settings


import json
import random
import uuid
import time
import datetime
import pytz
import urllib.request


def _check_user(token):
	if Token.objects.filter(token=token).exists():
		token = Token.objects.select_related('user').filter(token=token).order_by('-expire_time').first()
		# print('======',toke)
		print('======token',token.expire_time)
		print(datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC')))
		now = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
		if token.expire_time > now:
			return 1
		if not token.user:
			return 2
		token.expire_time = datetime.datetime.now() + datetime.timedelta(hours=3)
		token.save()
		return token

	else:
		return 0


def check_user(func):
	def view(token, *args, **kwargs):
		token = _check_user(token)

		print('=========',token)
		
		if isinstance(token,int):
			return {'code':-1, 'msg':token}

		return func(token, *args, **kwargs)
	# print(dir(view))#.name = func.name
	# print(dir(func))#.name = func.name
	view.__name__ = func.__name__
	return view


#获取手机验证码
@api
def get_code(phone):
	number = []

	for i in range(6):
		rand_num = random.randint(0,9)
		number.append(str(rand_num))
	num = ''.join(number)

	Verify.objects.create(phone=phone, code=num)

	return {'code':1,'msg':'已发送','phone_code':num}
	

#查询全部的国家
@api
def country_show(**name):
	ctx = {}
	ctx['list_country'] = list_country = []
	# first = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	country = Country.objects.all().order_by('name')
	one = Country.objects.filter(name__startswith=name)
	print(one)

	for i in country:
		d = {
			'name': i.name,
			'code': i.code,
			'logo': i.logo.url
		}
		list_country.append(d)

	# for j in country:
	# 	for i in first:
	# 		a = i
	# 		print('====j',j.name,'=====',i)
	# 		if i == j.name[:1]:
	# 			i = {
	# 				'id': j.id,
	# 				'name': j.name,
	# 				'code': j.code,
	# 				'logo': j.logo.url
	# 			}
	# 			print(i)

	# 			list_country.append(i)
	return list_country				




#登陆||注册
@api
def login(phone, code, id):
	#获取手机号和验证码查询手机验证码表最新数据
	verify = Verify.objects.filter(phone=phone, code=code).order_by('-create_time')[:1].first()
	country = Country.objects.filter(id=id).first()
	user = User.objects.filter(phone=phone).first()
	print('======',verify)
	print('======',country)
	print('======',user)

	#随机生成uuid
	uid = uuid.uuid1().hex
	#获取当前时间
	now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	date = datetime.datetime.strptime(now,'%Y-%m-%d %H:%M:%S')
	#token失效时间
	now_date = date + datetime.timedelta(hours=3)

	if verify == None:
		return {'code':-1,'msg':'验证码输入有误'}
	else:
		if not user:
			user = User.objects.create(
				phone = phone,
				country = country,
			)

			#创建token
			Token.objects.create(
				user = user,
				token = uid,
				expire_time = now_date
			)		
			return {'code':1,'msg':'创建成功', 'token':uid}
		else:
			#创建token
			Token.objects.create(
				user = user,
				token = uid,
				expire_time = now_date
			)			
			return {'code':2, 'msg':'登录成功', 'token':uid}


#第一次用户登陆之后需添加用户名
@check_user
@api
def createname(token, nickname, headphoto):

	headphoto = HeadPhoto.objects.filter(headimg=headphoto).first()
	
	user = User.objects.filter(id=token.user.id).first()

	print(user)

	unickname = User.objects.filter(nickname=nickname).first()

	if not unickname:
		user.nickname = nickname
		user.headphoto = headphoto
		user.save()
		return {'code':1, 'msg':'添加成功'}
	else:
		return {'code':-1, 'msg':'this dj name is taken or cannot be used please try another dj name'}


#
@api
@check_user
def mix_insert(token, cover, dname, mname):

	if token != None:
		user = User.objects.filter(id=token.user.id).first()

		image = Cover.objects.filter(cover=cover).first()

		Mix.objects.create(
			user = user,
			cover = image,
			dname = dname,
			mname = mname
		)
		return {'code':1, 'msg':'添加成功'}
	else:
		return {'code':-1, 'msg':'请重新登录'}


@api
@check_user
def music_show(token):

	ctx = {}
	mlist = []
	ctx['song'] = song = Song.objects.all()
	
	for _ in ctx['song']:
		d = {
			'id':_.id,
			'songname':_.songname,
			'song':_.song.url,
			'author':_.author,
			'cover': _.cover.url
		}
		mlist.append(d)
	print(mlist)

	return mlist


@api
@check_user
def choose_music(token, id=[1]):
	print('====',token.user.id)
	user = User.objects.filter(id=token.user.id).first()

	song = Song.objects.filter(id__in=id)

	mix = Mix.objects.create(
		user = user
	)
	for i in song:
		mix.song.add(i)

	return {'code':1, 'msg':'添加成功'}


@api
@check_user
def rank():

	mix = Mix.objects.all()

	return 
	



	

