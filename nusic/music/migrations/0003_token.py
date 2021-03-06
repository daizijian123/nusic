# Generated by Django 2.1.3 on 2019-03-06 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20190306_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100, verbose_name='uuid')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='登录时间')),
                ('expire_time', models.DateTimeField(blank=True, null=True, verbose_name='失效时间')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.User')),
            ],
            options={
                'verbose_name': 'token表',
                'verbose_name_plural': 'token表',
            },
        ),
    ]
