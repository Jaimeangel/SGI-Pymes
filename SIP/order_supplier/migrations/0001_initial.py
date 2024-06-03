# Generated by Django 4.2.13 on 2024-06-02 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock_product', '0001_initial'),
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(max_length=255)),
                ('total_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='OrderSupplierDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_supplier.ordersupplier')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_product.product')),
            ],
        ),
    ]