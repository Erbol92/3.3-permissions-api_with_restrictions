# Generated by Django 5.1.6 on 2025-02-10 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0002_favoriteadvertisement'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]
