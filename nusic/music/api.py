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
import random
import string


def _check_user(token):
	if Token.objects.filter(token=token).exists():
		token = Token.objects.select_related('user').filter(token=token).order_by('-expire_time').first()
		print('======',token)
		now = datetime.datetime.now()
		print('======token',token.expire_time)
		print('======now',now)
		if token.expire_time == None:
			return 1
		if token.expire_time < now :
			return 1
		if not token.user:
			return 2
		# token.expire_time = datetime.datetime.now() + datetime.timedelta(hours=3)
		# token.save()
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


@api
def code(phone):
	'''获取手机验证码'''
	number = []

	try:
		for i in range(6):
			rand_num = random.randint(0,9)
			number.append(str(rand_num))
		num = ''.join(number)

		Verify.objects.create(phone=phone, code=num)

		return {'status':0,'msg':'send successfully','phone_code':num}
	except :
		return {'status':1,'msg':'Send failure'}
	
	

@api
def country_show(**name):
	''' 查询全部的国家 '''

	ctx = {}
	ctx['list_country'] = list_country = []
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

	return list_country		



@api
def cover_show():
	''' 查询封面 '''

	cover = []

	image = Cover.objects.all()	

	for i in image:
		d = {
			"cover":i.cover.url,
			"cgold":i.cgold
		}

		cover.append(d)
	return {"code":1, "msg":cover}


#登陆||注册
@api
def login(phone, code, country_id=None):
	#获取手机号和验证码查询手机验证码表最新数据
	verify = Verify.objects.filter(phone=phone, code=code).order_by('-create_time')[:1].first()
	country = Country.objects.filter(id=country_id).first()
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
			return {'code':1, 'msg':'登录成功', 'token':uid}


#微信登陆
@api
def wechat(code):
	ctx = {}

	url = 'https://api.weixin.qq.com/sns/oauth2/access_token'

	params = {
		'appid':'wx3d59f92c7bf0d0f9',
		'secret':'04e6251c3b54340f68e693dafe761a0c',
		'code':code,
		'grant_type':'authorization_code'
	}

	wechat_response = requests.get(url,params=params).json()

	if 'access_token' not in wechat_response:
		return {"status":0,"msg":"登陆失败"}

	access_token = wechat_response['access_token']
	open_id = wechat_response['openid']

	user = User.objects.filter(open_id=open_id)
	if user.exists():
		ctx['user_id'] = user.first().id
		ctx['open_id'] = user.first().open_id
	else:
		user_info_params = {
			'access_token':access_token,
			'openid':open_id,
			'lang':'zh_CN'
		}

		user_info_url = 'https://api.weixin.qq.com/sns/userinfo'
		user_info = requests.get(user_info_url,params=user_info_params).content

		user_info = json.loads(user_info.decode('utf-8'))

		if 'nickname' not in user_info:
			return {"status":0,"msg":"登陆失败"}

		nickname = user_info['nickname']
		city = user_info['city']
		headimgurl = user_info['headimgurl']

		#获取当前时间
		now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		date = datetime.datetime.strptime(now,'%Y-%m-%d %H:%M:%S')
		#token失效时间
		now_date = date + datetime.timedelta(hours=3)

		user = User.objects.create(open_id=open_id, nickname=nickname, avatar_url=headimgurl, expire_time = now_date)
		ctx['user_id'] = user.id
		ctx['open_id'] = open_id
		print(open_id)

	return {'status':1, 'msg':'登录成功', 'token':uid}


@api
@check_user
def profile_edit(token, dj_name=None, logo_id=None):
	''' 用户补全信息 '''

	headphoto = HeadPhoto.objects.filter(id=logo_id).first()

	print(headphoto)
	
	user = User.objects.filter(id=token.user.id).first()

	print(user)

	if user:
		user.nickname = dj_name
		user.headphoto = headphoto
		user.save()
		return {'code':1, 'msg':'保存成功'}
	else:
		return {'code':-1, 'msg':'this dj name is taken or cannot be used please try another dj name'}


#
@api
@check_user
def mix_insert(token, id, dname, mname):

	if token != None:
		user = User.objects.filter(id=token.user.id).first()

		image = Cover.objects.filter(id=id).first()

		Mashups.objects.create(
			user = user,
			id = image,
			dname = dname,
			mname = mname
		)
		return {'code':1, 'msg':'添加成功'}
	else:
		return {'code':-1, 'msg':'请重新登录'}


@api
@check_user
def songs(token, page=1, page_size=20):
	ctx = []
	page-=1
	print(page)

	start = page_size*(page)

	song = Songs.objects.all().order_by('id')[start:start+page_size]


	print('start',start,'end',start+page_size)
	for _ in song:
		d = {
			'id':_.id,
			'songname':_.name,
			'artist':_.artist,
			'album': _.album,
			"album_cover":_.album_cover.url
		}
		ctx.append(d)

	return {'msg':ctx}


@api
@check_user
def mashup_create(token, main_song_id, other_song_ids=[]):
	'''选中歌曲后获取songs, tracks, cue_points '''

	result = {}
	main = {}
	other = []

	user = User.objects.filter(token=token.user.id).first()

	#主歌曲
	main_song = Songs.objects.filter(id=main_song_id).first()

	#创建混音
	mashups = Mashups.objects.create(main_song=main_song, user=user)
	# mashups.other_song.add(other_song__in=ctx)
	#混音多对多添加其他歌曲
	for i in other_song_ids:
		mashups.other_song.add(Songs.objects.filter(id=i).first())
	print(mashups)

	#创建游戏会话
	game_sessions = Game_sessions.objects.create(mashup=mashups)
	print(game_sessions)

	main = {
		"id":main_song.id,
		"name":main_song.name,
		"song":main_song.song.url,
		"artist":main_song.artist,
		"album":main_song.album,
		"album_cover":main_song.album_cover.url,
		"bpm":main_song.bpm
	}

	for j in other_song_ids:
		for k in Songs.objects.filter(id=j):
			d = {
				"id":k.id,
				"name":k.name,
				"song":k.song.url,
				"artist":k.artist,
				"album":k.album,
				"album_cover":k.album_cover.url,
				"bpm":k.bpm
			}

			other.append(d)

	result = {
		"mashup_id":mashups.id,
		"game_session_id":game_sessions.id,
		"main_song":main,
		"other_songs":other
	}

	return {"status":1, "result":result}

@api
@check_user
def rank():
	try:
		listp = []
		mashups = Mashups.objects.values('mname')
		print('----')
		for i in mashups:
			print(i)
			d = {
				'mashups':i.mname,
				'user':i.user.nickname
			}
			listp.append(d)
		print('===')

		return listp
	except:
		return {"code":-1, "msg":"错误"}


@api
@check_user
def mixable(token, song_id):
	''' 检索可混音的歌曲 '''

	#存储结果
	ctx = []
	#存储副歌曲id
	sid = []


	#查询音轨提示
	track_cues = Track_cues.objects.filter(primary_track_id__song__id=song_id)

	print(track_cues)

	for i in track_cues:
		print(i.secondary_track_id.song.id)
		sid.append(i.secondary_track_id.song.id)

	print(Songs.objects.filter(id__in=sid))

	song = Songs.objects.filter(id__in=sid)

	for i in song:
		d = {
			"id":i.id,
			"title":i.name,
			"artist":i.artist,
			"album":i.album,
			"album_cover":i.album_cover.url
		}

		ctx.append(d)


	return {"result":ctx}


@api
@check_user
def session_create(token, game_session_id, track_cues=[]):
	''' 游戏结束,保存用户行为信息 '''

	try:
		game_sessions = Game_sessions.objects.filter(id=game_session_id).first()

		print(game_sessions)

		for i in track_cues:
			Game_session_track_cues.objects.create(
				game_session_id = game_sessions,
				track_cue_id = Track_cues.objects.filter(id=i['track_cue_id']).first(),
				hit = i['hit']
			)

		return {'code' : 1, "msg":"Save success"}
	except:
		return {'code' : 0, "msg":"Save failed"}
	


@api
@check_user
def game_session(token, game_session_id):
	''' 获取gamesession '''
	ctx = []
	game_sessions = Game_sessions.objects.filter(mashup=game_session_id)

	for i in game_sessions:
		d = {
			'title':i.mashup.main_song.name,
			'album_cover':i.mashup.main_song.album_cover.url
		}

		ctx.append(d)

	for j in game_sessions.first().mashup.other_song.all():
		d = {
			'title':j.name,
			'album_cover':j.album_cover.url
		}
		ctx.append(d)


	return {'code':1, 'result':ctx}
	

@api
@check_user
def mashup_save(token, mashup_id, name, cover_id):
	''' 保存混音信息 '''

	try:

		#获取混音id
		mashups = Mashups.objects.filter(id=mashup_id).first()

		cover = Cover.objects.filter(id=cover_id).first()

		print(cover)

		mashups.name = name
		mashups.image = cover
		mashups.save()

		return {'status':1,'msg':'保存成功'}
	except:
		return {'status':0, 'msg':'保存失败'}


@api
def guest_login():
	''' 游客登陆 '''

	uid = uuid.uuid1().hex
	print(uid)

	
	nickname = ''.join(random.sample(string.ascii_letters + string.digits, 8))
	print(nickname)
	

	try:
		
		user = User.objects.create(
			nickname = nickname
		)

		#获取当前时间
		now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		date = datetime.datetime.strptime(now,'%Y-%m-%d %H:%M:%S')
		#token失效时间
		now_date = date + datetime.timedelta(hours=3)

		Token.objects.create(
			user = user,
			token = uid,
			expire_time = now_date
		)

		return {"status":1, "msg":"Visitors log in successfully", "token":uid}
	except :
		return {"status":0,"msg":"Tourists logon failure"}


@api
@check_user
def mashups(token, key=None, page=1, page_size=20):
	''' mashups '''
	ctx = []

	if key:
		mashups = Mashups.objects.filter(name__icontains=key)

		for j in mashups:
			d = {
				"id":j.id,
				"title":j.name,
				"artist":j.user.nickname if j.user else '',
				"album":"",
				"duration":j.duration,
				"album_cover":j.image.cover.url if j.image else ''
			}

			ctx.append(d)

	else:
		page-=1
		print(page)

		start = page_size*(page)

		mashup = Mashups.objects.all().order_by('id')[start:start+page_size]

		print('start',start,'end',start+page_size)

		for i in mashup:
			d = {
				"id":i.id,
				"title":i.name,
				"artist":i.user.nickname if i.user else '',
				"album":"",
				"duration":i.duration,
				"album_cover":i.image.cover.url if i.image else ''
			}

			ctx.append(d)

	return {"result":ctx}


@api
@check_user
def mashup(token, game_session_id):
	''' mashup '''

	game_sessions = Game_sessions.objects.filter(id=game_session_id).first()

	ctx = {
		"id":game_sessions.mashup.id,
		"title":game_sessions.mashup.name,
		"artist":game_sessions.mashup.user.nickname if game_sessions.mashup.user.nickname else '',
		"album":"",
		"duration":game_sessions.mashup.duration,
		"album_cover":game_sessions.mashup.image.cover.url if game_sessions.mashup.image.cover.url else '',
	}

	return {"result":ctx}


@api
@check_user
def profile_get(token):
	''' 获取用户信息 '''

	user = User.objects.filter(id=token.user.id).first()
	#获取当前时间
	now = datetime.datetime.now()
	#计算当前时间与创建时间相差天数
	day = (now - user.create_time).days

	sort = ''

	mashups = Mashups.objects.filter(user=user)
	print(user.create_time.year)
	print(mashups)
	
	if user:
		if user.openid:
			sort = '微信'
		if user.phone and user.country:
			sort = '手机号'
		if user.phone == None and user.openid == None:
			sort = '游客'


	ctx = {
		"dj_name":user.nickname if user.nickname else '',
		"headphoto":user.headphoto.headimg.url if user.headphoto != None else '',
		"avatar_url":user.avatar_url if user.avatar_url else '',
		"days":day,
		"start_year":user.create_time.year,
		"mash_ups":len(mashups) if len(mashups) else '',
		"type":sort
	}

	return {"result":ctx}


@api
@check_user
def logout(token):
	''' 用户退出登陆 '''

	result = {}

	try:
		user = User.objects.filter(id=token.user.id).first()

		token.expire_time = None
		token.save()

		result = {
			"status":1,
			"msg": "退出成功"
		}
		return result

	except:

		result = {
			"status":0,
			"msg":"退出失败"
		}

		return result


@api
@check_user
def requestsong(token, title, artist, recommended_remix, cover_id):
	''' 请求歌曲 '''

	user = User.objects.filter(id=token.user.id).first()

	cover = Cover.objects.filter(id=cover_id).first()

	try:
		
		RequestSong.objects.create(
			user = user,
			title = title,
			artist = artist,
			recommended_remix = recommended_remix,
			cover = cover
		)

		return {"status":1, "msg":"Thanks for your request!We’ll check it out!"}

	except:
		return {"status":0, "msg":"Could not submit request. Please try again later"}


@api
@check_user
def feedback(token, comments, contact=None, mashups_id=None):
	''' 问题 '''

	user = User.objects.filter(id=token.user.id).first()

	print(type(mashups_id))

	# try:
	if mashups_id:
		mashups_id = Mashups.objects.filter(id=mashups_id).first()
		print('===',mashups_id)

	FeedBack.objects.create(
		user = user,
		comments = comments,
		mashups = mashups_id if mashups_id else None,
		contact = contact if contact == True else False,
	)

	return {"status":1, "msg":"问题提交成功"}
	# except:
	# 	return {"status":0, "msg":"问题提交失败"}








			
	

	
	

