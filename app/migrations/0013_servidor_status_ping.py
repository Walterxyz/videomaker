# Generated by Django 4.2.4 on 2023-10-31 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_rename_datahoradelete_expurgo_datahoradeleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='servidor',
            name='status_ping',
            field=models.BooleanField(default=False),
        ),
    ]
