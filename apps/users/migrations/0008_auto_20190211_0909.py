# Generated by Django 2.1.5 on 2019-02-11 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='phone',
            field=models.CharField(max_length=255),
        ),
    ]
