# Generated by Django 2.1.7 on 2019-02-15 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20190215_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_challenge',
            field=models.BooleanField(default=True),
        ),
    ]
