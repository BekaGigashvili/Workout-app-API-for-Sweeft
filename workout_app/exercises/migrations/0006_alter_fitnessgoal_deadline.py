# Generated by Django 5.1.5 on 2025-02-04 11:06

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_rename_exercise_fitnessgoal_exercise_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessgoal',
            name='deadline',
            field=models.DateField(default=datetime.date(2025, 2, 4), validators=[django.core.validators.MinValueValidator(datetime.date(2025, 2, 4))]),
        ),
    ]
