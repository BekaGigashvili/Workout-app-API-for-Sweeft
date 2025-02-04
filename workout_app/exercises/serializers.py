from datetime import datetime
from rest_framework import serializers
from .models import Exercises, PersonalizedExercise, WorkoutPlan, WeightLog, FitnessGoal, WorkoutSession
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
    

class WorkoutSessionSerializer(serializers.ModelSerializer):
    personalized_exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=PersonalizedExercise.objects.all(),
        source='personalized_exercise',
        write_only=True,
        required=False,
        allow_null=True,
    )
    completed = serializers.BooleanField(default=False)
    current_sets = serializers.IntegerField(default=0)
    current_repetitions = serializers.IntegerField(default=0)

    class Meta:
        model = WorkoutSession
        fields = [
            'id', 
            'personalized_exercise_id', 
            'current_sets', 
            'current_repetitions', 
            'current_distance', 
            'completed',
            'created_at'
        ]
        read_only_fields = ['created_at']

    def validate(self, attrs):
        # Get the HTTP request method (POST, PUT, PATCH)
        request_method = self.context.get('request').method

        # If it's a POST request (creating a new WorkoutSession), make personalized_exercise required
        if request_method == 'POST':
            if 'personalized_exercise' not in attrs:
                raise serializers.ValidationError({"personalized_exercise": "This field is required."})

        # If personalized_exercise is provided, validate it
        personalized_exercise = attrs.get('personalized_exercise')
        if personalized_exercise:
            if attrs.get('current_sets') and attrs['current_sets'] > personalized_exercise.sets:
                raise serializers.ValidationError(
                    {"current_sets": f"Cannot exceed {personalized_exercise.sets} sets"}
                )
            if attrs.get('current_repetitions') and attrs['current_repetitions'] > personalized_exercise.repetitions:
                raise serializers.ValidationError(
                    {"current_repetitions": f"Cannot exceed {personalized_exercise.repetitions} reps"}
                )
            if attrs.get('current_distance') and personalized_exercise.distance:
                if attrs['current_distance'] > personalized_exercise.distance:
                    raise serializers.ValidationError(
                        {"current_distance": f"Cannot exceed {personalized_exercise.distance} km"}
                    )

        return attrs

    def update(self, instance, validated_data):
        instance.current_sets = validated_data.get('current_sets', instance.current_sets)
        instance.current_repetitions = validated_data.get('current_repetitions', instance.current_repetitions)
        instance.current_distance = validated_data.get('current_distance', instance.current_distance)

        if (instance.current_sets == instance.personalized_exercise.sets and 
            instance.current_repetitions == instance.personalized_exercise.repetitions) or \
           (instance.current_distance == instance.personalized_exercise.distance):
            instance.completed = True

        instance.save()
        return instance
