# Generated by Django 4.2.4 on 2023-10-30 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_expurgoservidores_is_password_encrypted'),
    ]

    operations = [
        migrations.AddField(
            model_name='expurgoservidores',
            name='apelido',
            field=models.CharField(default='remover', max_length=100),
            preserve_default=False,
        ),
    ]
