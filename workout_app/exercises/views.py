from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import WorkoutPlanSerializer, WeightLogSerializer
from .models import WorkoutPlan, WeightLog
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class WorkoutPlanCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=WorkoutPlanSerializer,
        responses={201: WorkoutPlanSerializer}
    )

    def post(self, request):
        serializer = WorkoutPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WorkoutPlanListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: WorkoutPlanSerializer(many=True)}
    )

    def get(self, request):
        workout_plans = WorkoutPlan.objects.filter(user=request.user)
        serializer = WorkoutPlanSerializer(workout_plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WeightLogCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            request_body=WeightLogSerializer,
            responses={201:WeightLogSerializer},
            operation_description="Log a new weight entry for the authenticated user."
    )
    def post(self, request):
        serializer = WeightLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class WeightLogGetView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: WeightLogSerializer(many=True)},
        operation_description="Get a list of all weight logs for the authenticated user."
    )
    def get(self, request):
        weight_logs = WeightLog.objects.filter(user = request.user).order_by('-date')
        serializer = WeightLogSerializer(weight_logs, many=True)
        return Response(serializer.data)