# Generated by Django 4.0 on 2022-05-02 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_App', '0003_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile',
            field=models.TextField(blank=True),
        ),
    ]