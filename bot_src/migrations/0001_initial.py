# Generated by Django 5.0.6 on 2024-05-28 16:41

import bot_src.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('processing', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to=bot_src.models.get_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='TelegramGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=300)),
                ('group_id', models.IntegerField(unique=True)),
            ],
        ),
    ]
