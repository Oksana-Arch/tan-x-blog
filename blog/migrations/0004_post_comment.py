# Generated by Django 2.2 on 2020-02-02 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200201_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comment',
            field=models.TextField(blank=True, max_length=150),
        ),
    ]