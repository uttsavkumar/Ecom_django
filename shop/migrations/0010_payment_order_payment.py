# Generated by Django 4.1.7 on 2023-03-17 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_address_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TXNID', models.CharField(max_length=200)),
                ('BANKTXNID', models.BigIntegerField()),
                ('ORDERID', models.CharField(max_length=20, unique=True)),
                ('TXNAMOUNT', models.FloatField()),
                ('STATUS', models.CharField(max_length=50)),
                ('TXNTYPE', models.CharField(max_length=20)),
                ('PAYMENTMODE', models.CharField(max_length=200)),
                ('REFUNDAMT', models.FloatField()),
                ('TXNDATE', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.payment'),
        ),
    ]
