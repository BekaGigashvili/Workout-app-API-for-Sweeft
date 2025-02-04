from django.urls import path
from .views import (
    WorkoutPlanListCreateAPIView,
    WeightLogListCreateAPIView,
    FitnessGoalListCreateAPIView,
)

urlpatterns = [
    path("workout-plans/", WorkoutPlanListCreateAPIView.as_view(), name="workout_plans"),
    path("weight-logs/", WeightLogListCreateAPIView.as_view(), name="weight_logs"),
    path("fitness-goals/", FitnessGoalListCreateAPIView.as_view(), name="fitness_goals"),
]
