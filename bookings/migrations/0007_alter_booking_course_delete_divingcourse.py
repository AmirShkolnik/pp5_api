# Generated by Django 5.0.6 on 2024-07-15 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_alter_booking_unique_together'),
        ('courses', '0007_course_excerpt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.DeleteModel(
            name='DivingCourse',
        ),
    ]