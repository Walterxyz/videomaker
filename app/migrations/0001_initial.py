# Generated by Django 4.2.4 on 2023-10-06 20:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servidor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('porta', models.PositiveIntegerField()),
                ('porta_ssh', models.PositiveIntegerField()),
                ('status', models.BooleanField()),
                ('service', models.CharField(max_length=100, null=True)),
                ('datahora', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Expurgo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('servidor', models.CharField(max_length=100)),
                ('base', models.CharField(max_length=100)),
                ('tabela', models.CharField(max_length=100)),
                ('tamanhomb', models.FloatField()),
                ('deletado', models.BooleanField()),
                ('datahora', models.DateTimeField(default=django.utils.timezone.now)),
                ('datahoradelete', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'unique_together': {('servidor', 'base', 'tabela')},
            },
        ),
    ]
