# Generated by Django 2.2.16 on 2021-08-26 06:14

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
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
                ('status', models.CharField(choices=[('new', 'новая'), ('planned', 'запланированная'), ('in_progress', 'в работе'), ('completed', 'завершенная')], max_length=11)),
                ('planned_finish', models.DateField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
