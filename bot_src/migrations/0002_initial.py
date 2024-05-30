# Generated by Django 5.0.6 on 2024-05-28 16:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bot_src', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='datasource',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_data', to='bot_src.collection'),
        ),
        migrations.AddField(
            model_name='collection',
            name='datasource',
            field=models.ManyToManyField(related_name='collection_data_source', to='bot_src.datasource'),
        ),
        migrations.AddField(
            model_name='telegramgroup',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collection',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bot_src.telegramgroup'),
        ),
    ]
