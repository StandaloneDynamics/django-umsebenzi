# Generated by Django 4.2 on 2023-12-11 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import umsebenzi.enums


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('code', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('status', django_enumfield.db.fields.EnumField(default=1, enum=umsebenzi.enums.ProjectStatus)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', django_enumfield.db.fields.EnumField(default=1, enum=umsebenzi.enums.TaskStatus)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_tasks', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='umsebenzi.project')),
            ],
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['code'], name='umsebenzi_t_code_dfb0b8_idx'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['title', 'code'], name='umsebenzi_p_title_49e8b5_idx'),
        ),
    ]
