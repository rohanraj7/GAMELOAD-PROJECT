# Generated by Django 4.1.3 on 2022-11-28 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gameadmin', '0008_remove_myorders_city_remove_myorders_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myorders',
            name='userid',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
