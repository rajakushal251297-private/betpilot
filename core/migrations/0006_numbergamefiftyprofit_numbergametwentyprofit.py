# Generated by Django 5.1.2 on 2024-11-17 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_depositdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumberGameFiftyProfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profit', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='NumberGameTwentyProfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profit', models.CharField(max_length=200)),
            ],
        ),
    ]