from datetime import datetime
from rest_framework import serializers
from .models import Exercises, PersonalizedExercise, WorkoutPlan, WeightLog, FitnessGoal
from django.core.validators import MinValueValidator


class ExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = '__all__'

class PersonalizedExerciseSerializer(serializers.ModelSerializer):
    exercise_id = serializers.PrimaryKeyRelatedField(queryset = Exercises.objects.all())
    sets = serializers.IntegerField(default=0)
    repetitions = serializers.IntegerField(default=0)
    duration = serializers.FloatField(default=0)
    distance = serializers.FloatField(default=0)

    class Meta:
        model = PersonalizedExercise
        fields = ['exercise_id', 'sets', 'repetitions', 'duration', 'distance']

    def validate(self, data):
        exercise = data.get('exercise_id')
        if not exercise.distance_related:
            if not (data.get('sets') > 0 and data.get('repetitions') > 0):
                raise serializers.ValidationError('Number of sets and repetitions must be greater than 0 for sets and repetitions related exercise.')
            if data.get('distance'):
                raise serializers.ValidationError('Distance can only be set for exercises related to distance.')
        if not exercise.sets_and_repetitions_related:
            if not data.get('distance') > 0 and not data.get('duration') > 0:
                raise serializers.ValidationError('Distance or Duration must be greater than 0 for distance related exercises.')
            if data.get('sets') or data.get('repetitions'):
                raise serializers.ValidationError('Sets and repetitions can only be set for exercises related to sets and repetitions.')
        return data
    
class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = PersonalizedExerciseSerializer(many=True)
    workout_frequency = serializers.IntegerField(default=1, min_value=1, max_value=7,)
    session_duration = serializers.IntegerField(default=5, min_value=5, max_value=1440)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'name', 'goal', 'workout_frequency', 'session_duration', 'exercises']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        workout_plan = WorkoutPlan.objects.create(**validated_data)
        for exercise_data in exercises_data:
            try:
                PersonalizedExercise.objects.create(workout_plan=workout_plan, **exercise_data)
            except Exception as e:
                workout_plan.delete()
                raise serializers.ValidationError(f"Error creating personalized exercise: {str(e)}")
        return workout_plan
    
class WeightLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightLog
        fields =['id', 'user', 'date', 'weight']
        read_only_fields = ['user']

class FitnessGoalSerializer(serializers.ModelSerializer):
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercises.objects.all(),
        required=False,
        allow_null=True
    )
    achieved = serializers.BooleanField(default=False)
    target_reps = serializers.IntegerField(
        default=0,
        min_value=0, max_value=15
    )
    target_sets = serializers.IntegerField(
        default=0,
        min_value=0, max_value=10
    ) 
    deadline = serializers.DateField() 

    class Meta:
        model = FitnessGoal
        fields = ['id', 'user', 'goal_type', 'target_weight', 'exercise_id', 'target_reps', 'target_sets', 'deadline', 'achieved']
        read_only_fields = ['user']

    def validate_deadline(self, value):
        if value < datetime.now().date():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value