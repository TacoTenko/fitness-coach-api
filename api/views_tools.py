from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SuggestSupplements(APIView):
    def get(self, request):
        """
        Could accept query params like ?diet=vegan or ?goal=gain_muscle
        """
        diet = request.GET.get('diet', 'omnivore')
        goal = request.GET.get('goal', 'general')
        # Hardcode or have a DB for supplement suggestions
        suggestions = []
        if goal == 'gain_muscle':
            suggestions.append("Whey Protein")
        if diet == 'vegan':
            suggestions.append("Vitamin B12")

        if not suggestions:
            suggestions.append("A general multivitamin")

        return Response({"supplements": suggestions})

class ValidateWorkoutPlan(APIView):
    def post(self, request):
        """
        Expects JSON with a list of workouts or muscle groups:
        {
            "workouts": ["Push-ups", "Squats", "Plank"]
        }
        """
        workouts = request.data.get('workouts', [])
        # Simplified check: do we have both upper and lower body workouts?
        upper_body = any("push" in w.lower() or "pull" in w.lower() for w in workouts)
        lower_body = any("squat" in w.lower() or "lunge" in w.lower() for w in workouts)
        if upper_body and lower_body:
            return Response({"balanced": True, "message": "Your workout plan is balanced."})
        return Response({"balanced": False, "message": "Consider adding more variety."})

class GenerateFitnessReport(APIView):
    def get(self, request, user_id):
        # Summarize user’s progress, recommended workouts, meal plans, etc.
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        logs = ProgressLog.objects.filter(user=user).order_by('-date')
        # Example summary
        total_workouts = sum(log.workouts_completed for log in logs)
        last_weight = logs[0].weight_kg if logs else user.weight_kg

        return Response({
            "username": user.username,
            "total_workouts_completed": total_workouts,
            "current_weight": last_weight,
            "message": "Keep up the good work!"
        })

class AlertMissingWorkouts(APIView):
    def get(self, request, user_id):
        # Check if user has no logs for the past X days
        from datetime import date, timedelta
        cutoff = date.today() - timedelta(days=3)
        logs = ProgressLog.objects.filter(user__id=user_id, date__gte=cutoff)
        if not logs.exists():
            return Response({"alert": True, "message": "You’ve missed workouts recently!"})
        return Response({"alert": False, "message": "No missing workouts."})
