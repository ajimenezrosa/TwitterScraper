# Generated by Django 2.0.5 on 2018-05-16 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('locations', models.TextField(blank=True, null=True)),
                ('personality', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
