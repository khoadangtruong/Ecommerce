# Generated by Django 2.2 on 2020-12-01 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_remove_product_on_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='on_sale',
            field=models.BooleanField(default=False),
        ),
    ]