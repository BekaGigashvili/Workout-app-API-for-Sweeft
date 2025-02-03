from django.db import models

class Exercises(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    instructions = models.TextField()
    target_muscles = models.CharField(max_length=200)
    equipment = models.CharField(max_length=100, blank=True, null=True)
    difficulty_level = models.CharField(max_length=100)
    distance_related = models.BooleanField(default=False)
    sets_and_repetitions_related = models.BooleanField(default=False)

    def __str__(self):
        return self.name