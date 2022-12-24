# Generated by Django 4.1.3 on 2022-11-30 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productmanagement', '0001_initial'),
        ('cartmanagement', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(max_length=200)),
                ('price', models.IntegerField(null=True)),
                ('image', models.ImageField(upload_to='pics')),
                ('description', models.CharField(max_length=750)),
                ('productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productmanagement.stock')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
