# Generated by Django 2.2.16 on 2021-08-26 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_taskhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskhistory',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='task.Task'),
        ),
    ]
