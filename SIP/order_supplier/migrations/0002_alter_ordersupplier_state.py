# Generated by Django 4.2.13 on 2024-06-05 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_supplier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersupplier',
            name='state',
            field=models.CharField(choices=[('INPROGRESS', 'INPROGRESS'), ('COMPLETED', 'COMPLETED')], default='INPROGRESS', max_length=10),
        ),
    ]