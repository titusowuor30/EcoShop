# Generated by Django 3.1.5 on 2021-02-01 16:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]