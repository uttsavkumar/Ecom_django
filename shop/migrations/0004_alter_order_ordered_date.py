# Generated by Django 4.1.7 on 2023-03-03 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]