# Generated by Django 5.1.6 on 2025-04-21 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume_parser', '0003_alter_resume_options_resume_experience'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resume',
            options={},
        ),
        migrations.RemoveField(
            model_name='resume',
            name='experience',
        ),
    ]
