# Generated by Django 4.0 on 2022-04-27 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='politician',
            name='party_logo',
            field=models.ImageField(blank=True, upload_to='party_logo/'),
        ),
    ]