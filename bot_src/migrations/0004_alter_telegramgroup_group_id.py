# Generated by Django 5.0.6 on 2024-05-28 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_src', '0003_remove_collection_datasource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramgroup',
            name='group_id',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
