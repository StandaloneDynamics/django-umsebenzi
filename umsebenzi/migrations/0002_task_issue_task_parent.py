# Generated by Django 4.2 on 2024-07-04 09:41

from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import umsebenzi.enums


class Migration(migrations.Migration):

    dependencies = [
        ('umsebenzi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='issue',
            field=django_enumfield.db.fields.EnumField(default=1, enum=umsebenzi.enums.Issue),
        ),
        migrations.AddField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='umsebenzi.task'),
        ),
    ]
