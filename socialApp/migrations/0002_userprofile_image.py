# Generated by Django 2.1.3 on 2018-12-17 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='', upload_to='profile_images'),
            preserve_default=False,
        ),
    ]