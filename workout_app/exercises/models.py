from django.db import models
from users.models import User
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.utils import timezone

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
    
class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    goal = models.CharField(max_length=255, unique=True)
    workout_frequency = models. IntegerField(
        help_text="Times per week",
        validators=[MinValueValidator(1), MaxLengthValidator(7)]
    )
    session_duration = models.IntegerField(
        help_text="Duration in minutes. Daily.",
        validators=[MinValueValidator(5), MaxLengthValidator(1440)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    
class PersonalizedExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='exercises')
    exercise_id = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    sets = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)]
        )
    repetitions = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    duration = models.FloatField(
        help_text='duration in hours',
        default=0,
        validators=[MinValueValidator(0)]
    )
    distance = models.FloatField(
        help_text="Distance in kilometers.",
        null = True, blank=True,
        validators=[MinValueValidator(0)]
    )

class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_logs')
    date = models.DateField(auto_now_add=True)
    weight = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    def __str__(self):
        return f'{self.user.username} - {self.weight} kg on {self.date}'
    
class FitnessGoal(models.Model):
    GOAL_TYPES = [
        ('weight', 'Weight Goal'),
        ('exercise', 'Exercise Achievement'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fitness_goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_weight = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)]) 
    exercise_id = models.ForeignKey(Exercises, on_delete=models.SET_NULL, null=True, blank=True) 
    target_reps = models.PositiveIntegerField(
        null=True, blank=True, default=0,
        validators=[MinValueValidator(0)]
    ) 
    target_sets = models.PositiveIntegerField(
        null=True, blank=True, default=0,
        validators=[MinValueValidator(0)]
    )
    deadline = models.DateField()  
    achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Goal - {self.get_goal_type_display()}"
