# Generated by Django 4.2.4 on 2023-11-30 20:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_slots_datahora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slots',
            name='datahora',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
