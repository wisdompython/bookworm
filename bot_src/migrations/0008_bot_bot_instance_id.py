# Generated by Django 5.0.6 on 2024-06-17 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_src', '0007_alter_bot_api_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='bot_instance_id',
            field=models.TextField(null=True),
        ),
    ]
