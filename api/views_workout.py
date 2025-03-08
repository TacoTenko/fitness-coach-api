from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Workout, ProgressLog, UserProfile
from .serializers import WorkoutSerializer, ProgressLogSerializer
import random


class RecommendWorkout(APIView):
    def get(self, request):
        # Example logic: pick a random workout
        workouts = Workout.objects.all()
        if workouts.exists():
            recommended = random.choice(workouts)
            return Response(WorkoutSerializer(recommended).data)
        return Response({"detail": "No workouts found."}, status=status.HTTP_404_NOT_FOUND)

class CalculateCaloriesBurned(APIView):
    def post(self, request):
        """
        Expects JSON like:
        {
            "workout_id": 1,
            "user_weight": 70
        }
        """
        workout_id = request.data.get('workout_id')
        user_weight = float(request.data.get('user_weight', 70))  # default weight
        try:
            workout = Workout.objects.get(id=workout_id)
            # Simple formula: base * user_weight / some factor
            calories_estimated = workout.duration_minutes * (user_weight / 70) * 5
            return Response({"calories_burned": calories_estimated})
        except Workout.DoesNotExist:
            return Response({"detail": "Workout not found."}, status=status.HTTP_404_NOT_FOUND)

class TrackExerciseProgress(APIView):
    def get(self, request, user_id):
        # Summarize a user's workout history from ProgressLog
        logs = ProgressLog.objects.filter(user__id=user_id)
        serializer = ProgressLogSerializer(logs, many=True)
        return Response(serializer.data)

class SuggestRestDays(APIView):
    def get(self, request, user_id):
        # Simplified logic: if user has completed workouts 3 days in a row, suggest a rest day
        logs = ProgressLog.objects.filter(user__id=user_id).order_by('-date')[:3]
        if all(log.workouts_completed > 0 for log in logs):
            return Response({"rest_days_recommended": 1})
        return Response({"rest_days_recommended": 0})

class GetStretchingRoutine(APIView):
    def get(self, request):
        # Return a static or random stretching routine
        routine = [
            "Neck Tilts x 10 reps",
            "Shoulder Rolls x 10 reps",
            "Hamstring Stretch 30s",
            "Calf Stretch 30s"
        ]
        return Response({"stretching_routine": routine})
