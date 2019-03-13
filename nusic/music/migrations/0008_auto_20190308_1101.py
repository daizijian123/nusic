# Generated by Django 2.1.3 on 2019-03-08 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_auto_20190307_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mix',
            name='song',
        ),
        migrations.AddField(
            model_name='mix',
            name='song',
            field=models.ManyToManyField(to='music.Song', verbose_name='组合音乐'),
        ),
    ]
