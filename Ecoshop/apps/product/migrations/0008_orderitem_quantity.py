# Generated by Django 3.1.5 on 2021-02-07 06:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0007_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
