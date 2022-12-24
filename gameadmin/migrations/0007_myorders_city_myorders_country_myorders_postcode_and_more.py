# Generated by Django 4.1.3 on 2022-11-28 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameadmin', '0006_remove_myorders_city_remove_myorders_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myorders',
            name='city',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='myorders',
            name='country',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='myorders',
            name='postcode',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='myorders',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
