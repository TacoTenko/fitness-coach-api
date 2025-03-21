# api/views_progress.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, ProgressLog, Workout
from .serializers import ProgressLogSerializer, WorkoutSerializer
from .services import (
    predict_goal_achievement,
    calculate_weekly_weight_change,
    compare_workouts,
    check_progress_trends,
    convert_units
)

class PredictGoalAchievement(APIView):
    def get(self, request, user_id):
        """
        GET /api/predict/goal-achievement/<user_id>/?target_weight=65
        """
        target_weight = request.query_params.get('target_weight')
        if not target_weight:
            return Response({"detail": "Please provide target_weight in query params."}, status=400)

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        result = predict_goal_achievement(user, float(target_weight))
        if result:
            return Response(result)
        return Response({"detail": "Unable to predict goal."}, status=400)

class CalculateWeightLossGain(APIView):
    def post(self, request):
        """
        Expects JSON:
        {
            "current_weight": 70,
            "goal_weight": 65
        }
        """
        current_weight = float(request.data.get('current_weight', 70))
        goal_weight = float(request.data.get('goal_weight', 65))
        weekly_change = calculate_weekly_weight_change(current_weight, goal_weight)
        return Response({"weekly_weight_change": weekly_change})

class TrackWeightProgress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST /api/track/weight-progress/
        {
            "user_id": 1,
            "weight_kg": 69,
            "workouts_completed": 2,
            "notes": "Felt good today!"
        }
        """
        user_id = request.data.get('user_id')
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        log = ProgressLog.objects.create(
            user=user,
            weight_kg=request.data.get('weight_kg', 0),
            workouts_completed=request.data.get('workouts_completed', 0),
            notes=request.data.get('notes', '')
        )
        return Response(ProgressLogSerializer(log).data, status=201)

class CompareWorkouts(APIView):
    def get(self, request):
        """
        GET /api/compare/workouts/?workout1=1&workout2=2
        """
        w1_id = request.GET.get('workout1')
        w2_id = request.GET.get('workout2')
        try:
            w1 = Workout.objects.get(id=w1_id)
            w2 = Workout.objects.get(id=w2_id)
        except Workout.DoesNotExist:
            return Response({"detail": "One or both workouts not found."}, status=404)

        comparison = compare_workouts(w1, w2)
        return Response(comparison)

class CheckProgressTrends(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        trend = check_progress_trends(user_id)
        return Response({"trend": trend})

class ConvertMeasurementUnits(APIView):
    def get(self, request):
        """
        GET /api/convert/measurement-units/?value=70&unit=kg
        """
        value = float(request.GET.get('value', 0))
        unit = request.GET.get('unit', 'kg')
        result = convert_units(value, unit)
        return Response(result)
