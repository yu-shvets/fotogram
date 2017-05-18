# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 14:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('author', models.CharField(max_length=256, verbose_name='Author')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
            ],
            options={
                'verbose_name_plural': 'Comments',
                'ordering': ['-datetime'],
                'verbose_name': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('photo', models.ImageField(upload_to='', verbose_name='Photo')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('like', models.IntegerField(blank=True, default=0, verbose_name='Like')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Posts',
                'ordering': ['-datetime'],
                'verbose_name': 'Post',
            },
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fotogram_app.Posts'),
        ),
    ]
