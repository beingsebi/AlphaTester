# Generated by Django 4.1 on 2024-04-16 17:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backtester", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="strategy",
            name="strategyDetails",
            field=models.JSONField(null=True),
        ),
    ]
