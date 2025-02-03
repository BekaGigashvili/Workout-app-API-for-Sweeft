from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import WorkoutPlanSerializer, WorkoutPlan
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