# Generated by Django 2.2 on 2020-11-15 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_contactmessage_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='phonenumber',
        ),
    ]