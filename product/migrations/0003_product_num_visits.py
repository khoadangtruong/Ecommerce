# Generated by Django 2.2 on 2020-11-23 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_last_visit'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_visits',
            field=models.IntegerField(default=0),
        ),
    ]
