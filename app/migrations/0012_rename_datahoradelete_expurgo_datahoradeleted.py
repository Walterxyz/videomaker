# Generated by Django 4.2.4 on 2023-10-30 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_expurgo_datahoratodelete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expurgo',
            old_name='datahoradelete',
            new_name='datahoradeleted',
        ),
    ]
