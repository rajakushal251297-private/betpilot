# Generated by Django 5.1.2 on 2024-11-21 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_numbergamefiftyprofit_numbergametwentyprofit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorGameTimeAdd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
            ],
        ),
    ]
