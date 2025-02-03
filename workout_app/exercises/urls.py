from django.urls import path
from .views import WorkoutPlanCreateView, WorkoutPlanListView

urlpatterns = [
    path('workout-plans/', WorkoutPlanListView.as_view(), name='workout-plans-list'),
    path('workout-plans/create/', WorkoutPlanCreateView.as_view(), name='workout-plan-create'),
]