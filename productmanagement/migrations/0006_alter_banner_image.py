# Generated by Django 4.1.3 on 2022-12-17 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productmanagement', '0005_alter_banner_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(upload_to='pics/'),
        ),
    ]
