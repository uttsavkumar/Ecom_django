# Generated by Django 4.1.7 on 2023-03-14 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_address_order_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='email',
        ),
        migrations.AddField(
            model_name='address',
            name='contact',
            field=models.CharField(max_length=254, null=True),
        ),
    ]
