from django.forms import ValidationError
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import WorkoutPlan, WeightLog, FitnessGoal, WorkoutSession
from .serializers import (
    WorkoutPlanSerializer,
    WeightLogSerializer,
    FitnessGoalSerializer,
    WorkoutSessionSerializer,
)


class WorkoutPlanListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkoutPlanSerializer

    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        request_body=WorkoutPlanSerializer, responses={201: WorkoutPlanSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: WorkoutPlanSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class WeightLogListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WeightLogSerializer

    def get_queryset(self):
        return WeightLog.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        request_body=WeightLogSerializer,
        responses={201: WeightLogSerializer},
        operation_description="Log a new weight entry for the authenticated user.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: WeightLogSerializer(many=True)},
        operation_description="Get a list of all weight logs for the authenticated user.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FitnessGoalListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FitnessGoalSerializer

    def get_queryset(self):
        return FitnessGoal.objects.filter(user=self.request.user).order_by("-deadline")

    def perform_create(self, serializer):
        data = self.request.data.copy()

        serializer = FitnessGoalSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        request_body=FitnessGoalSerializer,
        responses={201: FitnessGoalSerializer},
        operation_description="Log a new fitness goal entry for the authenticated user.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: FitnessGoalSerializer(many=True)},
        operation_description="Get a list of all fitness goal logs for the authenticated user.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class WorkoutSessionCreateAPIView(ListCreateAPIView):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        personalized_exercise = serializer.validated_data['personalized_exercise']
        if personalized_exercise.workout_plan.user != self.request.user:
            raise ValidationError('You dont own this exercise')

        serializer.save(user=self.request.user)

class WorkoutSessionUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkoutSessionSerializer
    http_method_names = ['put'] 

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return WorkoutSession.objects.none()
        return WorkoutSession.objects.filter(user=self.request.user)