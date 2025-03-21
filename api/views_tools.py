# api/views_tools.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .services import (
    suggest_supplements,
    validate_workout_plan,
    generate_fitness_report,
    alert_missing_workouts
)

class SuggestSupplements(APIView):
    def get(self, request):
        """
        GET /api/suggest/supplements/?diet=vegan&goal=gain_muscle
        """
        diet = request.GET.get('diet', 'omnivore')
        goal = request.GET.get('goal', 'general')
        suggestions = suggest_supplements(diet, goal)
        return Response({"supplements": suggestions})

class ValidateWorkoutPlan(APIView):
    def post(self, request):
        """
        POST /api/validate/workout-plan/
        {
            "workouts": ["Push-ups", "Squats", "Plank"]
        }
        """
        workouts = request.data.get('workouts', [])
        balanced = validate_workout_plan(workouts)
        if balanced:
            return Response({"balanced": True, "message": "Workout plan is balanced."})
        return Response({"balanced": False, "message": "Consider adding more variety."})

class GenerateFitnessReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        """
        GET /api/generate/fitness-report/<user_id>/
        """
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        report = generate_fitness_report(user)
        return Response(report)

class AlertMissingWorkouts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        """
        GET /api/alert/missing-workouts/<user_id>/
        """
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        missing = alert_missing_workouts(user)
        return Response({
            "alert": missing,
            "message": "You’ve missed workouts recently!" if missing else "No missing workouts."
        })
