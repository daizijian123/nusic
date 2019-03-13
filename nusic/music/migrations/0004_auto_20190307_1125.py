# Generated by Django 2.1.3 on 2019-03-07 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='mix',
            name='song',
            field=models.FileField(blank=True, null=True, upload_to='mixsong', verbose_name='组合音乐'),
        ),
        migrations.AddField(
            model_name='song',
            name='song',
            field=models.FileField(blank=True, null=True, upload_to='song', verbose_name='歌曲'),
        ),
    ]
