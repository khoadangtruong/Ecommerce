# Generated by Django 2.2 on 2020-11-27 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_comment_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='image',
        ),
    ]
