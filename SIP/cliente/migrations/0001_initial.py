# Generated by Django 4.2.13 on 2024-06-01 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('identity', models.CharField(max_length=255)),
                ('phone_contact', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
    ]