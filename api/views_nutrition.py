from .models import MealPlan, UserProfile
from .serializers import MealPlanSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RecommendDailyCalories(APIView):
    def post(self, request):
        """
        Expects JSON like:
        {
            "user_id": 1,
            "goal": "lose_weight" or "maintain" or "gain_weight"
        }
        """
        user_id = request.data.get('user_id')
        goal = request.data.get('goal', 'maintain')

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Very basic formula
        base_calories = 2000
        if goal == "lose_weight":
            base_calories -= 300
        elif goal == "gain_weight":
            base_calories += 300

        # Adjust for user stats if you like
        recommended = base_calories
        return Response({"recommended_calories_per_day": recommended})

class SuggestMealPlan(APIView):
    def get(self, request):
        """
        Optionally accept query params like ?type=low-carb
        """
        meal_type = request.GET.get('type', 'default')
        # Filter or randomly pick from MealPlan model
        plans = MealPlan.objects.all()
        if meal_type != 'default':
            plans = plans.filter(plan_name__icontains=meal_type)

        if plans.exists():
            plan = random.choice(plans)
            return Response(MealPlanSerializer(plan).data)
        return Response({"detail": "No meal plans found."}, status=status.HTTP_404_NOT_FOUND)

class CalculateMacros(APIView):
    def post(self, request):
        """
        Expects JSON like:
        {
            "calories": 2000,
            "ratio": {"protein": 0.3, "fat": 0.2, "carbs": 0.5}
        }
        """
        calories = request.data.get('calories', 2000)
        ratio = request.data.get('ratio', {"protein": 0.3, "fat": 0.2, "carbs": 0.5})
        # 1g protein = 4 cal, 1g carb = 4 cal, 1g fat = 9 cal
        protein_cals = calories * ratio["protein"]
        fat_cals = calories * ratio["fat"]
        carb_cals = calories * ratio["carbs"]

        return Response({
            "protein_g": round(protein_cals / 4, 2),
            "fat_g": round(fat_cals / 9, 2),
            "carbs_g": round(carb_cals / 4, 2),
        })

class FindHealthySnacks(APIView):
    def get(self, request):
        # Hardcode or query from DB
        snacks = [
            "Apple slices with peanut butter",
            "Greek yogurt with berries",
            "Carrot sticks with hummus",
            "Nuts and seeds mix"
        ]
        return Response({"healthy_snacks": snacks})

class ValidateHydration(APIView):
    def post(self, request):
        """
        Expects JSON like:
        {
            "user_id": 1,
            "water_intake_liters": 1.5
        }
        """
        water_intake = float(request.data.get('water_intake_liters', 0))
        if water_intake < 2:
            return Response({"hydration_ok": False, "message": "Drink more water!"})
        return Response({"hydration_ok": True, "message": "Hydration on track."})
