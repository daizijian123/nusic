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


class User(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '用户'
		db_table = "user"


	nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
	phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='手机号')
	openid = models.CharField(max_length=200, blank=True, null=True, verbose_name='openid')
	avatar_url = models.CharField(max_length=200, blank=True, null=True, verbose_name='微信头像')

	country = models.ForeignKey('Country', blank=True, null=True, on_delete=models.CASCADE, verbose_name='国家')
	gold = models.IntegerField(blank=True, null=True,verbose_name='金币')
	headphoto = models.ForeignKey('HeadPhoto', blank=True, null=True, verbose_name='头像', on_delete=models.CASCADE)

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Token(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = 'token表'
		db_table = "token"

	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	token = models.CharField(max_length=100, verbose_name='uuid')
	
	create_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
	expire_time = models.DateTimeField(blank=True, null=True, verbose_name='失效时间')


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
		indexes = [
			models.Index(
			fields=['name'],
			name='index_songs_on_name',
			),
		]

	name = models.CharField(max_length=50, verbose_name='歌曲名称')
	song = models.FileField(upload_to='song/', blank=True, null=True, verbose_name='歌曲')
	artist = models.CharField(max_length=50, verbose_name='作者')
	album = models.CharField(max_length=100, verbose_name='专辑')
	album_cover = models.ImageField(upload_to='songcover/', verbose_name='歌曲封面')
	bpm = models.FloatField(verbose_name='bpm')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Tracks(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '音轨'
		db_table = 'tracks'

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

	uuid = models.CharField(max_length=200, verbose_name='uuid')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Mashups(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '混音'
		db_table = "mashups"

	name = models.CharField(max_length=50, blank=True, null=True, verbose_name='混音名称')
	description = models.TextField(null=True,verbose_name='描述')
	blink_time = models.IntegerField(null=True,verbose_name='闪烁时间')
	max_score = models.IntegerField(null=True,verbose_name='最大成绩')
	passing_score = models.IntegerField(null=True,verbose_name='合格成绩')
	duration = models.IntegerField(null=True,verbose_name='持续时间')
	bpm = models.IntegerField(null=True,verbose_name='bpm')
	level = models.IntegerField(blank=True, null=True, verbose_name='星级')
	score = models.IntegerField(blank=True, null=True, verbose_name='评分')
	like = models.IntegerField(blank=True, null=True, verbose_name='点赞')
	dislike = models.IntegerField(blank=True, null=True, verbose_name='不喜欢')
	main_song = models.ForeignKey(Songs, null=True, verbose_name='组合音乐', on_delete=models.CASCADE, related_name='main_song')
	other_song = models.ManyToManyField(Songs, verbose_name='组合音乐', related_name='other_song')
	image = models.ForeignKey(Cover, blank=True, null=True, verbose_name='封面', on_delete=models.SET_NULL)
	user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户', on_delete=models.CASCADE)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Game_sessions(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '游戏会话'
		db_table = 'game_sessions'

	mashup = models.ForeignKey(Mashups, on_delete=models.CASCADE)
	device = models.ForeignKey(Devices, null=True, on_delete=models.CASCADE) 
	score = models.IntegerField(null=True, verbose_name='分数')
	file_path = models.FileField(null=True, upload_to='game_sessions/', verbose_name='文件路径')
	avg_proximity = models.FloatField(null=True, verbose_name='平均接近')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Game_session_track_cues(models.Model):

	class Meta:
		verbose_name = verbose_name_plural = '游戏会话轨迹提示'
		db_table = 'game_session_track_cues'

	game_session_id = models.ForeignKey(Game_sessions, on_delete=models.CASCADE)
	track_cue_id = models.ForeignKey(Track_cues, on_delete=models.CASCADE)
	hit = models.BooleanField(verbose_name='hit')
	proximity = models.IntegerField(null=True, verbose_name='接近')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Shop(models.Model):
	pass


class RequestSong(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '请求歌曲'
		db_table = 'feedback'

	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
	title = models.CharField(max_length=200, verbose_name='名称')
	artist = models.CharField(max_length=100, verbose_name='作者')
	recommended_remix = models.CharField(max_length=200, verbose_name='推荐混音')
	cover = models.ForeignKey(Cover, on_delete=models.CASCADE, verbose_name='封面')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class FeedBack(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '问题'
		db_table = 'problem'

	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
	mashups = models.ForeignKey(Mashups, null=True, blank=True, on_delete=models.CASCADE, verbose_name='混音')
	comments = models.TextField(default='', verbose_name='问题')
	contact = models.BooleanField(null=True, blank=True, verbose_name='是否联系用户')





