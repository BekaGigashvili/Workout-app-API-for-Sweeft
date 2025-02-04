from django.urls import path
from .views import WorkoutPlanCreateView, WorkoutPlanListView, WeightLogGetView, WeightLogCreateView

urlpatterns = [
    path('workout-plans/', WorkoutPlanListView.as_view(), name='workout-plans-list'),
    path('workout-plans/create/', WorkoutPlanCreateView.as_view(), name='workout-plan-create'),
    path('weight-logs/', WeightLogGetView.as_view(), name='weight_logs'),
    path('weight-logs/create/', WeightLogCreateView.as_view(), name='weight_logs'),
]