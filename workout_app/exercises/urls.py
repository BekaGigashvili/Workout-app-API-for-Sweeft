from django.urls import path
from .views import (
    WorkoutPlanListCreateAPIView,
    WeightLogListCreateAPIView,
    FitnessGoalListCreateAPIView,
    WorkoutSessionCreateAPIView,
    WorkoutSessionUpdateAPIView,

)

urlpatterns = [
    path("workout-plans/", WorkoutPlanListCreateAPIView.as_view(), name="workout_plans"),
    path("weight-logs/", WeightLogListCreateAPIView.as_view(), name="weight_logs"),
    path("fitness-goals/", FitnessGoalListCreateAPIView.as_view(), name="fitness_goals"),
    path('workout-sessions/', WorkoutSessionCreateAPIView.as_view(), name='workout-sessions'),
    path('workout_sessions/<int:pk>/update/', WorkoutSessionUpdateAPIView.as_view(), name='update-workout-session'),

]
