from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PredictGoalAchievement(APIView):
    def get(self, request, user_id):
        """
        Returns a naive 'goal date' if user wants to lose/gain weight
        by ~0.5 kg/week, for example.
        """
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Example logic: user wants to lose 5 kg at 0.5 kg/week => 10 weeks
        # We'll just assume user has a 'target_weight' in the future
        target_weight = user.weight_kg - 5  # example
        weeks_needed = abs(user.weight_kg - target_weight) / 0.5

        return Response({
            "estimated_weeks_to_goal": round(weeks_needed),
            "estimated_date": "YYYY-MM-DD (calculate from now + weeks_needed)"
        })

class CalculateWeightLossGain(APIView):
    def post(self, request):
        """
        Expects JSON like:
        {
            "current_weight": 70,
            "goal_weight": 65
        }
        """
        current_weight = float(request.data.get('current_weight', 70))
        goal_weight = float(request.data.get('goal_weight', 65))
        difference = goal_weight - current_weight
        # e.g., lose/gain difference over 10 weeks
        weekly_change = difference / 10
        return Response({"weekly_weight_change": round(weekly_change, 2)})

class TrackWeightProgress(APIView):
    def post(self, request):
        """
        Expects JSON like:
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
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        log = ProgressLog.objects.create(
            user=user,
            weight_kg=request.data.get('weight_kg', 0),
            workouts_completed=request.data.get('workouts_completed', 0),
            notes=request.data.get('notes', '')
        )
        return Response(ProgressLogSerializer(log).data, status=status.HTTP_201_CREATED)

class CompareWorkouts(APIView):
    def get(self, request):
        """
        Expects query params: ?workout1=1&workout2=2
        Compares two workouts in terms of calories, duration, etc.
        """
        w1_id = request.GET.get('workout1')
        w2_id = request.GET.get('workout2')
        try:
            w1 = Workout.objects.get(id=w1_id)
            w2 = Workout.objects.get(id=w2_id)
        except Workout.DoesNotExist:
            return Response({"detail": "One or both workouts not found."}, status=status.HTTP_404_NOT_FOUND)

        comparison = {
            "workout1": WorkoutSerializer(w1).data,
            "workout2": WorkoutSerializer(w2).data,
            "calories_diff": w1.calories_burned_estimate - w2.calories_burned_estimate,
            "duration_diff": w1.duration_minutes - w2.duration_minutes
        }
        return Response(comparison)

class CheckProgressTrends(APIView):
    def get(self, request, user_id):
        logs = ProgressLog.objects.filter(user__id=user_id).order_by('-date')[:5]
        # Example: check if user’s weight is decreasing or workouts_completed is increasing
        if len(logs) < 2:
            return Response({"trend": "Insufficient data"})
        # Simple logic: compare latest two logs
        latest = logs[0]
        previous = logs[1]
        if latest.weight_kg < previous.weight_kg:
            trend = "Weight decreasing"
        else:
            trend = "Weight stable or increasing"

        return Response({"trend": trend})

class ConvertMeasurementUnits(APIView):
    def get(self, request):
        """
        Query params:
        ?value=70&unit=kg => returns lbs
        ?value=180&unit=cm => returns inches
        """
        value = float(request.GET.get('value', 0))
        unit = request.GET.get('unit', 'kg')
        if unit == 'kg':
            converted = value * 2.20462  # kg -> lbs
            return Response({"value_in_lbs": round(converted, 2)})
        elif unit == 'lbs':
            converted = value / 2.20462  # lbs -> kg
            return Response({"value_in_kg": round(converted, 2)})
        elif unit == 'cm':
            converted = value / 2.54    # cm -> inches
            return Response({"value_in_inches": round(converted, 2)})
        elif unit == 'inches':
            converted = value * 2.54   # inches -> cm
            return Response({"value_in_cm": round(converted, 2)})
        else:
            return Response({"detail": "Invalid unit."}, status=status.HTTP_400_BAD_REQUEST)
