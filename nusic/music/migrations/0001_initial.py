# Generated by Django 2.1.3 on 2019-03-06 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='国家名称')),
                ('logo', models.ImageField(upload_to='countrylogo', verbose_name='国家logo')),
                ('code', models.CharField(max_length=50, verbose_name='区域码')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '国家',
                'verbose_name_plural': '国家',
            },
        ),
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='cover', verbose_name='封面')),
                ('cgold', models.IntegerField(verbose_name='金币')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '封面',
                'verbose_name_plural': '封面',
            },
        ),
        migrations.CreateModel(
            name='Gold',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gold', models.IntegerField(verbose_name='金币')),
                ('money', models.IntegerField(verbose_name='购买金额')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '金币',
                'verbose_name_plural': '金币',
            },
        ),
        migrations.CreateModel(
            name='HeadPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headimg', models.ImageField(blank=True, null=True, upload_to='headimg', verbose_name='头像')),
                ('hgold', models.IntegerField(verbose_name='金币')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '头像',
                'verbose_name_plural': '头像',
            },
        ),
        migrations.CreateModel(
            name='Mix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dname', models.CharField(blank=True, max_length=50, null=True, verbose_name='dj名称')),
                ('mname', models.CharField(blank=True, max_length=50, null=True, verbose_name='组合名称')),
                ('level', models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='星级')),
                ('score', models.IntegerField(blank=True, null=True, verbose_name='评分')),
                ('like', models.IntegerField(blank=True, null=True, verbose_name='点赞')),
                ('dislike', models.IntegerField(blank=True, null=True, verbose_name='不喜欢')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('cover', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Cover', verbose_name='封面')),
            ],
            options={
                'verbose_name': '组合',
                'verbose_name_plural': '组合',
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('songname', models.CharField(max_length=50, verbose_name='歌曲名称')),
                ('author', models.CharField(max_length=50, verbose_name='作者')),
                ('cover', models.ImageField(upload_to='songcover', verbose_name='歌曲封面')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '歌曲',
                'verbose_name_plural': '歌曲',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=50, null=True, verbose_name='昵称')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='手机号')),
                ('gold', models.IntegerField(verbose_name='金币')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Country', verbose_name='国家')),
                ('headphoto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.HeadPhoto', verbose_name='头像')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('code', models.CharField(max_length=50, verbose_name='验证码')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '手机验证码',
                'verbose_name_plural': '手机验证码',
            },
        ),
        migrations.AddField(
            model_name='mix',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.User', verbose_name='用户'),
        ),
    ]
