# Generated by Django 4.1.3 on 2022-12-12 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameadmin', '0011_alter_user_is_superuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(max_length=150)),
                ('coupon_code', models.CharField(max_length=150)),
                ('added_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('validtill', models.DateTimeField()),
                ('minimum_price', models.IntegerField()),
                ('discount', models.IntegerField()),
            ],
        ),
    ]
