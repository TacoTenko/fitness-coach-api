
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserProfile, MealPlan
from .serializers import MealPlanSerializer
from .services import (
    recommend_daily_calories,
    suggest_meal_plan,
    calculate_macros,
    find_healthy_snacks,
    validate_hydration
)

class RecommendDailyCalories(APIView):
    def post(self, request):
        """
        Expects JSON:
        {
            "user_id": 1,
            "goal": "lose_weight"
        }
        """
        user_id = request.data.get('user_id')
        goal = request.data.get('goal', 'maintain')
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        recommended = recommend_daily_calories(user, goal)
        return Response({"recommended_calories_per_day": recommended})

class SuggestMealPlan(APIView):
    def get(self, request):
        """
        GET /api/suggest/meal-plan/?type=low-carb
        """
        meal_type = request.GET.get('type', 'default')
        plan = suggest_meal_plan(meal_type)
        if plan:
            return Response(MealPlanSerializer(plan).data)
        return Response({"detail": "No meal plans found."}, status=status.HTTP_404_NOT_FOUND)

class CalculateMacros(APIView):
    def post(self, request):
        """
        Expects JSON:
        {
            "calories": 2000,
            "ratio": {"protein":0.3,"fat":0.2,"carbs":0.5}
        }
        """
        calories = int(request.data.get('calories', 2000))
        ratio = request.data.get('ratio', {"protein": 0.3, "fat": 0.2, "carbs": 0.5})
        result = calculate_macros(calories, ratio)
        return Response(result)

class FindHealthySnacks(APIView):
    def get(self, request):
        snacks = find_healthy_snacks()
        return Response({"healthy_snacks": snacks})

class ValidateHydration(APIView):
    def post(self, request):
        """
        Expects JSON:
        {
            "water_intake_liters": 1.5
        }
        """
        water_intake = float(request.data.get('water_intake_liters', 0))
        ok, message = validate_hydration(water_intake)
        return Response({"hydration_ok": ok, "message": message})
