# Generated by Django 5.0.6 on 2024-07-12 13:14

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0003_remove_contact_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='deletion_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
