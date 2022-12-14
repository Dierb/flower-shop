# Generated by Django 4.1.2 on 2022-12-11 23:21

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', colorfield.fields.ColorField(default='#F0000', image_field=None, max_length=18, samples=None)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('details_and_care', models.TextField(blank=True)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('price', models.IntegerField(default=1)),
                ('visits', models.IntegerField(default=0)),
                ('size', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('stars', models.IntegerField(choices=[(1, '???????????????'), (2, '???????????????'), (3, '???????????????'), (4, '???????????????'), (5, '???????????????')], default=3)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
