from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import random
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
        # 1. Get the "level" query param, default to "beginner" if not provided
        fitness_level = request.query_params.get('level', 'beginner')

        # 2. Filter workouts by that fitness level
        workouts = Workout.objects.filter(fitness_level=fitness_level)

        # 3. If we have workouts, pick one at random; otherwise, return 404
        if workouts.exists():
            recommended = random.choice(workouts)
            return Response(WorkoutSerializer(recommended).data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": f"No workouts found for fitness level '{fitness_level}'."},
                status=status.HTTP_404_NOT_FOUND
            )

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
    permission_classes = [IsAuthenticated]  # Optional if global default is set

    def get(self, request):
        # Automatically use the authenticated user from the token
        user = request.user
        logs = ProgressLog.objects.filter(user=user)
        serializer = ProgressLogSerializer(logs, many=True)
        return Response(serializer.data)

class SuggestRestDays(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET /api/suggest/rest-days/<user_id>/
        """
        logs = ProgressLog.objects.filter(user=request.user).order_by('-date')[:3]
        user_id = request.user.id
        days = suggest_rest_days(user_id)
        return Response({"rest_days_recommended": days})

class GetStretchingRoutine(APIView):
    def get(self, request):
        routine = get_stretching_routine()
        return Response({"stretching_routine": routine})

class WorkoutListCreateView(generics.ListCreateAPIView):
    """
    GET: List all workouts.
    POST: Create a new workout.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class WorkoutListByLevelView(generics.ListAPIView):
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        level = self.request.query_params.get('level', 'beginner')
        return Workout.objects.filter(fitness_level=level)

class WorkoutDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific workout by its ID.
    PUT/PATCH: Update a workout.
    DELETE: Delete a workout.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
