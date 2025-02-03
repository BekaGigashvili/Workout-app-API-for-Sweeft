from django.core.management.base import BaseCommand
from exercises.models import Exercises

class Command(BaseCommand):
    help = 'Populate the exercises table with initial data'

    def handle(self, *args, **kwargs):
        exercises=[
            {
                "name": 'Push-up',
                "description": 'A bodyweight exercise.',
                "instructions": 'Start in a high plank, lower yourself, and push back up',
                "target_muscles": 'Chest, Triceps, Shoulders',
                "equipment": 'None',
                "difficulty_level": 'Beginner',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": 'Squat',
                "description": 'Lower body movement.',
                "instructions": 'Bend knees, lower hips, andpush back up.',
                "target_muscles": 'Glutes, Hamstrings.',
                "equipment": 'None',
                "difficulty_level": 'Beginner',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": 'Deadlift',
                "description": 'A strength training exercise.',
                "instructions": 'Lift a barbell from the ground by extending hips and knees.',
                "target_muscles": 'Glutes, lower back',
                "equipment": 'Barbell',
                "difficulty_level": 'Advanced',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": 'Pull-up',
                "description": 'An upper body exercise.',
                "instructions": 'Hang from a bar and pull your chin over it.',
                "target_muscles": 'Back, Biceps.',
                "equipment": 'Pull up bar',
                "difficulty_level": 'Intermediate',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": 'Running',
                "description": 'Cardio strengthening exercise.',
                "instructions": 'Run freely',
                "target_muscles": 'Hamstrings, Glutes, Legs.',
                "equipment": 'None',
                "difficulty_level": 'Beginner',
                "distance_related": True,
                "sets_and_repetitions_related": False
            },
            {
                "name": "Bench Press",
                "description": "A classic strength training exercise for the chest.",
                "instructions": "Lie on a bench and push a barbell upward.",
                "target_muscles": "Chest, Triceps, Shoulders",
                "equipment": 'Barbell',
                "difficulty_level": 'Intermediate',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "swimming",
                "description": "Cardio and full body strengthening exercise.",
                "instructions": "Swim freely.",
                "target_muscles": "full body",
                "equipment": 'None',
                "difficulty_level": 'Intermediate',
                "distance_related": True,
                "sets_and_repetitions_related": False
            },
            {
                "name": "Bicep Curl",
                "description": "An isolation exercise for the biceps.",
                "instructions": "Curl a dumbbell or barbell towards your shoulders.",
                "target_muscles": "Biceps",
                "equipment": 'Dumbell',
                "difficulty_level": 'Beginner',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "Tricep Dips",
                "description": "A bodyweight triceps exercise.",
                "instructions": "Lower your body on parallel bars and push back up.",
                "target_muscles": "Triceps, Shoulders",
                "equipment": 'None',
                "difficulty_level": 'Intermediate',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "Leg Press",
                "description": "A machine-based lower body exercise.",
                "instructions": "Push the platform away with your legs.",
                "target_muscles": "Quadriceps, Hamstrings, Glutes",
                "equipment": 'Machine',
                "difficulty_level": 'Intermediate',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "Cycling",
                "description": "Cardio and legs strengthening exercise.",
                "instructions": "Sit on a bicycle and cycle freely.",
                "target_muscles": "Hamstrings, legs",
                "equipment": 'Bicycle',
                "difficulty_level": 'Beginner',
                "distance_related": True,
                "sets_and_repetitions_related": False
            },
            {
                "name": "Shoulder Press",
                "description": "A compound shoulder movement.",
                "instructions": "Press a barbell or dumbbells overhead.",
                "target_muscles": "Shoulders, Triceps",
                "equipment": 'Dumbell',
                "difficulty_level": 'Intermediate',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "Burpees",
                "description": "A full-body cardio and strength move.",
                "instructions": "Squat down, jump back, push-up, jump up.",
                "target_muscles": "Full Body",
                "equipment": 'None',
                "difficulty_level": 'Intermediate',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "Calf Raises",
                "description": "Strengthens the lower legs.",
                "instructions": "Rise onto toes and lower back down.",
                "target_muscles": "Calves",
                "equipment": 'None',
                "difficulty_level": 'Beginner',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "Lat Pulldown",
                "description": "A back-strengthening machine exercise.",
                "instructions": "Pull a bar down towards your chest.",
                "target_muscles": "Back, Biceps",
                "equipment": 'Machine',
                "difficulty_level": 'Beginner',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "Hanging Leg Raises",
                "description": "A core exercise using a pull-up bar.",
                "instructions": "Hang from a bar and raise legs to a 90-degree angle.",
                "target_muscles": "Abs, Hip Flexors",
                "equipment": 'Pull Up Bar',
                "difficulty_level": 'Intermediate',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "Romanian Deadlift",
                "description": "A hamstring-dominant variation of deadlifts.",
                "instructions": "Lower the bar with a slight knee bend, then rise back up.",
                "target_muscles": "Hamstrings, Glutes, Lower Back",
                "equipment": 'Barbell',
                "difficulty_level": 'Advanced',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "Mountain Climbers",
                "description": "A cardio and core bodyweight exercise.",
                "instructions": "Run in a push-up position, bringing knees towards the chest.",
                "target_muscles": "Core, Shoulders, Legs",
                "equipment": 'None',
                "difficulty_level": 'Beginner',
                "distance_related": True,
                "sets_and_repetitions_related": False
            },
            {
                "name": "Jump Rope",
                "description": "A cardio-intensive full-body exercise.",
                "instructions": "Jump over a rope continuously.",
                "target_muscles": "Calves, Shoulders, Core",
                "equipment": 'None',
                "difficulty_level": 'Beginner',
                "distance_related": False,
                "sets_and_repetitions_related": True
            },
            {
                "name": "Face Pulls",
                "description": "An exercise for shoulder health and posture.",
                "instructions": "Pull a cable rope towards your face.",
                "target_muscles": "Shoulders, Upper Back",
                "equipment": 'Cable',
                "difficulty_level": 'Intermediate',
                "distance_related": False,
                "sets_and_repetitions_related": True
            } 
        ]

        try:
            for exercise in exercises:
                Exercises.objects.create(**exercise)
                print(f"Populated with {exercise['name']}")
            print('Database has been populated successfully!')
        except Exception as e:
            print(f'Error occurred during database population: {e}')

