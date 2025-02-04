# Generated by Django 5.1.5 on 2025-02-04 14:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutsession',
            name='personalized_exercise',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='exercises.personalizedexercise'),
        ),
    ]
