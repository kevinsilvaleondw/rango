# Generated by Django 3.1.2 on 2020-10-06 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
                ('model', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('views', models.IntegerField(default=0)),
            ],
        ),
    ]
