# Generated by Django 4.1 on 2024-06-14 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtester', '0004_instrument_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='results',
            field=models.JSONField(null=True),
        ),
    ]