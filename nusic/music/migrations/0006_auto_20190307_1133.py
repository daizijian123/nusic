# Generated by Django 2.1.3 on 2019-03-07 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_auto_20190307_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='logo',
            field=models.ImageField(upload_to='media/countrylogo/', verbose_name='国家logo'),
        ),
        migrations.AlterField(
            model_name='cover',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='media/cover/', verbose_name='封面'),
        ),
        migrations.AlterField(
            model_name='headphoto',
            name='headimg',
            field=models.ImageField(blank=True, null=True, upload_to='media/headimg/', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='mix',
            name='song',
            field=models.FileField(blank=True, null=True, upload_to='media/mixsong/', verbose_name='组合音乐'),
        ),
        migrations.AlterField(
            model_name='song',
            name='cover',
            field=models.ImageField(upload_to='media/songcover/', verbose_name='歌曲封面'),
        ),
        migrations.AlterField(
            model_name='song',
            name='song',
            field=models.FileField(blank=True, null=True, upload_to='media/song/', verbose_name='歌曲'),
        ),
    ]
