from django.db import models

# Create your models here.

class Verify(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '手机验证码'
		db_table = "verify"

	phone = models.CharField(max_length=11, verbose_name='手机号')
	code = models.CharField(max_length=50, verbose_name='验证码')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Gold(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '金币'
		db_table = "gold"


	gold = models.IntegerField(verbose_name='金币')
	money = models.IntegerField(verbose_name='购买金额')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Country(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '国家'
		db_table = "country"


	name = models.CharField(max_length=50, blank=True, null=True, verbose_name='国家名称')
	logo = models.ImageField(upload_to='countrylogo/', verbose_name='国家logo')
	code = models.CharField(max_length=50, verbose_name='区域码')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class HeadPhoto(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '头像'
		db_table = "headPhoto"


	headimg = models.ImageField(upload_to='headimg/', blank=True, null=True, verbose_name='头像')
	hgold = models.IntegerField(verbose_name='金币')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class User(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '用户'
		db_table = "user"


	nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
	phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='手机号')
	country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE, verbose_name='国家')
	gold = models.IntegerField(blank=True, null=True,verbose_name='金币')
	headphoto = models.ForeignKey(HeadPhoto, blank=True, null=True, verbose_name='头像', on_delete=models.CASCADE)

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Cover(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '封面'
		db_table = "cover"

	cover = models.ImageField(upload_to='cover/', blank=True, null=True, verbose_name='封面')
	cgold = models.IntegerField(verbose_name='金币')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Songs(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '歌曲'
		db_table = "songs"

	name = models.CharField(max_length=50, verbose_name='歌曲名称')
	song = models.FileField(upload_to='song/', blank=True, null=True, verbose_name='歌曲')
	artist = models.CharField(max_length=50, verbose_name='作者')
	album = models.CharField(max_length=100, verbose_name='专辑')
	album_cover = models.ImageField(upload_to='songcover/', verbose_name='歌曲封面')
	bpm = models.FloatField(verbose_name='bpm')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Mashups(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '混音'
		db_table = "mashups"

	id = models.AutoField(primary_key=True)
	image = models.ImageField(upload_to='Mashups/cover/', verbose_name='封面')
	file_path = models.FileField(upload_to='Mashups/', default='', verbose_name='混音音乐')
	name = models.CharField(max_length=50, blank=True, null=True, verbose_name='混音名称')
	description = models.TextField(verbose_name='描述')
	blink_time = models.IntegerField(verbose_name='闪烁时间')
	max_score = models.IntegerField(verbose_name='最大成绩')
	passing_score = models.IntegerField(verbose_name='合格成绩')
	duration = models.IntegerField(verbose_name='持续时间')
	bpm = models.IntegerField(verbose_name='bpm')
	# level = models.IntegerField(choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], blank=True, null=True, verbose_name='星级')
	# score = models.IntegerField(blank=True, null=True, verbose_name='评分')
	# like = models.IntegerField(blank=True, null=True, verbose_name='点赞')
	# dislike = models.IntegerField(blank=True, null=True, verbose_name='不喜欢')
	# song = models.ManyToManyField(Song, verbose_name='组合音乐')
	# image = models.ForeignKey(Cover, blank=True, null=True, verbose_name='封面', on_delete=models.CASCADE)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Score(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '评分'

	level = models.IntegerField(choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], blank=True, null=True, verbose_name='星级')
	score = models.IntegerField(blank=True, null=True, verbose_name='评分')
	dname = models.CharField(max_length=50, blank=True, null=True, verbose_name='dj名称')
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='用户')



class Mashup_Songs(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '混音歌曲'
		db_table = "mashup_songs"

		# indexes = [
		# 	models.Index(
		# 		fields=['id'],
		# 		name='mashup_songs_pkey',
		# 	),
		# 	models.Index(
		# 		fields=['song_id'],
		# 		name='mashup_songs_id',
		# 	),
		# 	models.Index(
		# 		fields=['mashup_id'],
		# 		name='mashup_mashup_id',
		# 	),
		# ]

	id = models.AutoField(primary_key=True)
	mashup_id = models.ForeignKey(Mashups, on_delete=models.CASCADE, verbose_name='混音')
	song_id = models.ForeignKey(Songs, on_delete=models.CASCADE, verbose_name='歌曲')
	mashup_song_type = models.CharField(max_length=50, verbose_name='混音类型')


class Token(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = 'token表'
		db_table = "token"

	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	token = models.CharField(max_length=100, verbose_name='uuid')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
	expire_time = models.DateTimeField(blank=True, null=True, verbose_name='失效时间')


class Shop(models.Model):
	pass


class Tracks(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '音轨'
		db_table = 'tracks'
		# indexes = [
		# 	models.Index(
		# 		fields=['id'],
		# 		name='id_idx',
		# 	),
		# 	models.Index(
		# 		fields=['song'],
		# 		name='song_idx',
		# 	),
		# ]

	id = models.AutoField(primary_key=True)
	song = models.ForeignKey(Songs, blank=True, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=True, null=True, verbose_name='名称')
	file_path = models.FileField(upload_to='Tracks/', verbose_name='音轨')
	duration = models.IntegerField(blank=True, null=True, verbose_name='持续时间')
	description = models.TextField(blank=True, null=True, verbose_name='描述')
	track_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='音轨类型')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Track_cues(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '音轨提示'
		db_table = 'track_cues'
		# indexes = [
		# 	models.Index(
		# 		fields=['id'],
		# 		name='track_cues_pkey',
		# 	)
		# ]

	id = models.AutoField(primary_key=True)
	primary_track_id = models.ForeignKey(Tracks, blank=True, null=True, on_delete=models.CASCADE, related_name='primary_track_id')
	secondary_track_id = models.ForeignKey(Tracks, blank=True, null=True, on_delete=models.CASCADE, related_name='secondary_track_id')
	match_score = models.FloatField(blank=True, null=True, verbose_name='匹配分数')
	primary_track_start = models.IntegerField(blank=True, null=True, verbose_name='主音轨开始')
	primary_track_end = models.IntegerField(blank=True, null=True, verbose_name='主音轨结束')
	secondary_track_start = models.IntegerField(blank=True, null=True, verbose_name='次音轨开始')
	secondary_track_end = models.IntegerField(blank=True, null=True, verbose_name='次音轨结束')
	primary_track_beat_start = models.IntegerField(blank=True, null=True, verbose_name='主音轨敲击开始')
	primary_track_beat_end = models.IntegerField(blank=True, null=True, verbose_name='主音轨敲击结束')
	secondary_track_beat_start = models.IntegerField(blank=True, null=True, verbose_name='次音轨敲击开始')
	secondary_track_beat_end = models.IntegerField(blank=True, null=True, verbose_name='次音轨敲击结束')
	semitone_shift = models.IntegerField(blank=True, null=True, verbose_name='半音程转变')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Devices(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '设备'
		db_table = 'devices'
		# indexes = [
		# 	models.Index(
		# 		fields=['id'],
		# 		name='devices_pkey',
		# 	)
		# ]

	id = models.AutoField(primary_key=True)
	uuid = models.CharField(max_length=200, verbose_name='uuid')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Game_sessions(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '游戏会话'
		db_table = 'game_sessions'
		# indexes = [
		# 	models.Index(
		# 		fields=['id'],
		# 		name='game_sessions_pkey',
		# 	),
		# 	models.Index(
		# 		fields=['device_id'],
		# 		name='game_sdevice_id',
		# 	),
		# 	models.Index(
		# 		fields=['mashup_id'],
		# 		name='game_mashups_id',
		# 	),
		# ]

	id = models.AutoField(primary_key=True)
	mashup_id = models.ForeignKey(Mashups, on_delete=models.CASCADE)
	device_id = models.ForeignKey(Devices, on_delete=models.CASCADE)	
	score = models.IntegerField(verbose_name='分数')
	file_path = models.FileField(upload_to='game_sessions/', verbose_name='文件路径')
	avg_proximity = models.FloatField(verbose_name='平均接近')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Game_session_track_cues(models.Model):

	class Meta:
		verbose_name = verbose_name_plural = '游戏会话轨迹提示'
		db_table = 'game_session_track_cues'
		#联合约束
		# unique_together = ["track_cue_id","game_session_id"]
		# #联合索引
		# index_together = ["track_cue_id","game_session_id"]
		# indexes = [
		# 	models.Index(
		# 		fields=['id'],
		# 		name='gstc_pkey',
		# 	),
		# 	models.Index(
		# 		fields=['game_session_id'],
		# 		name='game_sessions_cue_id',
		# 	),
		# 	models.Index(
		# 		fields=['track_cue_id'],
		# 		name='game_track_cues_id',
		# 	),
		# ]

	id = models.AutoField(primary_key=True)
	game_session_id = models.ForeignKey(Game_sessions, on_delete=models.CASCADE)
	track_cue_id = models.ForeignKey(Track_cues, on_delete=models.CASCADE)
	hit = models.BooleanField(verbose_name='hit')
	proximity = models.IntegerField(verbose_name='接近')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)











