# Generated by Django 5.0.3 on 2024-03-12 07:57

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('govisewana_login', '0003_profile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('2492f9bf-60d6-4473-a9f9-4a8592a65af7')),
        ),
    ]
