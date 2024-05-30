# Generated by Django 5.0.6 on 2024-05-30 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_src', '0005_bot'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramgroup',
            name='group',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='telegramgroup',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_src.bot')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_src.collection')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_src.telegramgroup')),
            ],
        ),
    ]
