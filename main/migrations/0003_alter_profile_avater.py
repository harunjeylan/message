# Generated by Django 4.0 on 2022-03-20 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_profile_avater'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avater',
            field=models.ImageField(default='user/avater.png', null=True, upload_to='user/avater'),
        ),
    ]
