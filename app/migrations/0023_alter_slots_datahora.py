# Generated by Django 4.2.4 on 2023-11-30 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_slots_datahora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slots',
            name='datahora',
            field=models.DateTimeField(default=None),
        ),
    ]
