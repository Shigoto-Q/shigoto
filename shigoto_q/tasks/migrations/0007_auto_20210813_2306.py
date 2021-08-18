# Generated by Django 3.1.7 on 2021-08-13 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_taskimage_command'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskimage',
            name='command',
            field=models.CharField(help_text='Command to execute after image startup.', max_length=255, verbose_name='Command to execute'),
        ),
    ]
