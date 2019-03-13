from django.db import models

# Create your models here.

class Verify(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '手机验证码'

	phone = models.CharField(max_length=11, verbose_name='手机号')
	code = models.CharField(max_length=50, verbose_name='验证码')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Gold(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '金币'

	gold = models.IntegerField(verbose_name='金币')
	money = models.IntegerField(verbose_name='购买金额')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Country(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '国家'

	name = models.CharField(max_length=50, blank=True, null=True, verbose_name='国家名称')
	logo = models.ImageField(upload_to='countrylogo/', verbose_name='国家logo')
	code = models.CharField(max_length=50, verbose_name='区域码')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class HeadPhoto(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '头像'

	headimg = models.ImageField(upload_to='headimg/', blank=True, null=True, verbose_name='头像')
	hgold = models.IntegerField(verbose_name='金币')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class User(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '用户'

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

	cover = models.ImageField(upload_to='cover/', blank=True, null=True, verbose_name='封面')
	cgold = models.IntegerField(verbose_name='金币')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)





class Song(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '歌曲'

	songname = models.CharField(max_length=50, verbose_name='歌曲名称')
	song = models.FileField(upload_to='song/', blank=True, null=True, verbose_name='歌曲')
	author = models.CharField(max_length=50, verbose_name='作者')
	cover = models.ImageField(upload_to='songcover/', verbose_name='歌曲封面')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Mix(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '组合'

	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='用户')
	cover = models.ForeignKey(Cover, blank=True, null=True, verbose_name='封面', on_delete=models.CASCADE)
	song = models.ManyToManyField(Song, verbose_name='组合音乐')
	mix = models.FileField(upload_to='mix/', default='', verbose_name='混音音乐')
	dname = models.CharField(max_length=50, blank=True, null=True, verbose_name='dj名称')
	mname = models.CharField(max_length=50, blank=True, null=True, verbose_name='组合名称')
	level = models.IntegerField(choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], blank=True, null=True, verbose_name='星级')
	score = models.IntegerField(blank=True, null=True, verbose_name='评分')
	like = models.IntegerField(blank=True, null=True, verbose_name='点赞')
	dislike = models.IntegerField(blank=True, null=True, verbose_name='不喜欢')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


class Token(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = 'token表'

	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	token = models.CharField(max_length=100, verbose_name='uuid')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
	expire_time = models.DateTimeField(blank=True, null=True, verbose_name='失效时间')


class Shop(models.Model):
	pass




