# Generated by Django 5.0.6 on 2024-05-30 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_src', '0006_telegramgroup_group_telegramgroup_private_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='api_key',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]