from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Workout, ProgressLog
from .serializers import WorkoutSerializer, ProgressLogSerializer
from .services import (
    get_random_workout,
    calculate_calories_burned,
    get_stretching_routine,
    suggest_rest_days
)

class RecommendWorkout(APIView):
    def get(self, request):
        workout = get_random_workout()
        if workout:
            return Response(WorkoutSerializer(workout).data)
        return Response({"detail": "No workouts found."}, status=status.HTTP_404_NOT_FOUND)

class CalculateCaloriesBurned(APIView):
    def post(self, request):
        """
        Expects JSON:
        {
            "workout_id": 1,
            "user_weight": 70
        }
        """
        workout_id = request.data.get('workout_id')
        user_weight = float(request.data.get('user_weight', 70))
        try:
            workout = Workout.objects.get(id=workout_id)
        except Workout.DoesNotExist:
            return Response({"detail": "Workout not found."}, status=status.HTTP_404_NOT_FOUND)

        calories = calculate_calories_burned(workout, user_weight)
        return Response({"calories_burned": calories})

class TrackExerciseProgress(APIView):
    def get(self, request, user_id):
        """
        GET /api/track/exercise-progress/<user_id>/
        Returns progress logs for a user.
        """
        logs = ProgressLog.objects.filter(user__id=user_id)
        serializer = ProgressLogSerializer(logs, many=True)
        return Response(serializer.data)

class SuggestRestDays(APIView):
    def get(self, request, user_id):
        """
        GET /api/suggest/rest-days/<user_id>/
        """
        days = suggest_rest_days(user_id)
        return Response({"rest_days_recommended": days})

class GetStretchingRoutine(APIView):
    def get(self, request):
        routine = get_stretching_routine()
        return Response({"stretching_routine": routine})
