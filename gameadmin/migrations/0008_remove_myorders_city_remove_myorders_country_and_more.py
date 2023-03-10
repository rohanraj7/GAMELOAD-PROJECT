# Generated by Django 4.1.3 on 2022-11-28 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gameadmin', '0007_myorders_city_myorders_country_myorders_postcode_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myorders',
            name='city',
        ),
        migrations.RemoveField(
            model_name='myorders',
            name='country',
        ),
        migrations.RemoveField(
            model_name='myorders',
            name='postcode',
        ),
        migrations.AlterField(
            model_name='myorders',
            name='address',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='gameadmin.address'),
            preserve_default=False,
        ),
    ]
