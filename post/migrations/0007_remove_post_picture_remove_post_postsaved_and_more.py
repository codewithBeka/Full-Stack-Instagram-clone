# Generated by Django 5.0.6 on 2024-06-25 11:33

import django.db.models.deletion
import post.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_alter_post_picture'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='post',
            name='postsaved',
        ),
        migrations.RemoveField(
            model_name='post',
            name='userlike',
        ),
        migrations.CreateModel(
            name='PostFileContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=post.models.user_directory_path)),
                ('file_type', models.CharField(blank=True, max_length=10, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.ManyToManyField(related_name='contents', to='post.postfilecontent'),
        ),
    ]
