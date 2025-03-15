# api/services.py

import random
from datetime import date, timedelta
from .models import Workout, ProgressLog, UserProfile, MealPlan

# ------------------------------
# WORKOUT SERVICES
# ------------------------------
def get_random_workout():
    """
    Returns a random workout from the database, or None if empty.
    """
    workouts = Workout.objects.all()
    return random.choice(workouts) if workouts.exists() else None

def calculate_calories_burned(workout, user_weight):
    """
    Calculates estimated calories burned.
    Example formula: duration_minutes * (user_weight / 70) * 5
    """
    return workout.duration_minutes * (user_weight / 70) * 5

def get_stretching_routine():
    """
    Returns a preset list of stretching exercises.
    """
    return [
        "Neck Tilts x 10 reps",
        "Shoulder Rolls x 10 reps",
        "Hamstring Stretch 30s",
        "Calf Stretch 30s"
    ]

def suggest_rest_days(user_id):
    """
    Example: if user has completed workouts for the last 3 days, suggest rest.
    """
    logs = ProgressLog.objects.filter(user__id=user_id).order_by('-date')[:3]
    if all(log.workouts_completed > 0 for log in logs):
        return 1
    return 0

# ------------------------------
# NUTRITION SERVICES
# ------------------------------
def recommend_daily_calories(user, goal='maintain'):
    """
    Basic formula to recommend daily calories.
    """
    base_calories = 2000
    if goal == 'lose_weight':
        base_calories -= 300
    elif goal == 'gain_weight':
        base_calories += 300
    # Optionally adjust further using user stats.
    return base_calories

def suggest_meal_plan(meal_type='default'):
    """
    Return a random MealPlan that matches meal_type or None if not found.
    """
    plans = MealPlan.objects.all()
    if meal_type != 'default':
        plans = plans.filter(plan_name__icontains=meal_type)
    return random.choice(plans) if plans.exists() else None

def calculate_macros(calories, ratio):
    """
    ratio example: {"protein": 0.3, "fat": 0.2, "carbs": 0.5}
    1g protein/carb = 4 cal, 1g fat = 9 cal
    """
    protein_cals = calories * ratio["protein"]
    fat_cals = calories * ratio["fat"]
    carb_cals = calories * ratio["carbs"]
    return {
        "protein_g": round(protein_cals / 4, 2),
        "fat_g": round(fat_cals / 9, 2),
        "carbs_g": round(carb_cals / 4, 2),
    }

def find_healthy_snacks():
    """
    Return a static list of snack suggestions.
    """
    return [
        "Apple slices with peanut butter",
        "Greek yogurt with berries",
        "Carrot sticks with hummus",
        "Nuts and seeds mix"
    ]

def validate_hydration(water_intake):
    """
    Example threshold: 2 liters per day
    """
    if water_intake < 2:
        return False, "Drink more water!"
    return True, "Hydration on track."

# ------------------------------
# PROGRESS MONITORING SERVICES
# ------------------------------
def predict_goal_achievement(user, target_weight):
    """
    Example: user wants to lose/gain difference at 0.5 kg/week.
    """
    if not user.weight_kg or not target_weight:
        return None
    weeks_needed = abs(user.weight_kg - target_weight) / 0.5
    estimated_date = date.today() + timedelta(weeks=weeks_needed)
    return {
        "estimated_weeks_to_goal": round(weeks_needed),
        "estimated_date": estimated_date.isoformat()
    }

def calculate_weekly_weight_change(current_weight, goal_weight):
    """
    Return difference / 10 for a 10-week plan, as an example.
    """
    difference = goal_weight - current_weight
    return round(difference / 10, 2)

def compare_workouts(workout1, workout2):
    """
    Compare workouts by duration and calories_burned_estimate.
    """
    return {
        "workout1": {
            "id": workout1.id,
            "name": workout1.name,
            "calories_burned_estimate": workout1.calories_burned_estimate,
            "duration_minutes": workout1.duration_minutes,
        },
        "workout2": {
            "id": workout2.id,
            "name": workout2.name,
            "calories_burned_estimate": workout2.calories_burned_estimate,
            "duration_minutes": workout2.duration_minutes,
        },
        "calories_diff": workout1.calories_burned_estimate - workout2.calories_burned_estimate,
        "duration_diff": workout1.duration_minutes - workout2.duration_minutes
    }

def check_progress_trends(user_id):
    """
    Example: checks the last 2 logs to see if weight is decreasing.
    """
    logs = ProgressLog.objects.filter(user__id=user_id).order_by('-date')[:2]
    if len(logs) < 2:
        return "Insufficient data"
    latest, previous = logs[0], logs[1]
    if latest.weight_kg < previous.weight_kg:
        return "Weight decreasing"
    return "Weight stable or increasing"

def convert_units(value, unit):
    """
    Supports kg ↔ lbs, cm ↔ inches
    """
    if unit == 'kg':
        return {"value_in_lbs": round(value * 2.20462, 2)}
    elif unit == 'lbs':
        return {"value_in_kg": round(value / 2.20462, 2)}
    elif unit == 'cm':
        return {"value_in_inches": round(value / 2.54, 2)}
    elif unit == 'inches':
        return {"value_in_cm": round(value * 2.54, 2)}
    else:
        return {"detail": "Invalid unit"}

# ------------------------------
# ADDITIONAL FITNESS TOOLS
# ------------------------------
def suggest_supplements(diet='omnivore', goal='general'):
    suggestions = []
    if goal == 'gain_muscle':
        suggestions.append("Whey Protein")
    if diet == 'vegan':
        suggestions.append("Vitamin B12")
    if not suggestions:
        suggestions.append("General multivitamin")
    return suggestions

def validate_workout_plan(workouts):
    """
    Basic check for upper & lower body mention.
    """
    upper_body = any("push" in w.lower() or "pull" in w.lower() for w in workouts)
    lower_body = any("squat" in w.lower() or "lunge" in w.lower() for w in workouts)
    return upper_body and lower_body

def generate_fitness_report(user):
    """
    Summarize total workouts completed & latest weight.
    """
    logs = ProgressLog.objects.filter(user=user).order_by('-date')
    total_workouts = sum(log.workouts_completed for log in logs)
    last_weight = logs[0].weight_kg if logs.exists() else user.weight_kg
    return {
        "username": user.username,
        "total_workouts_completed": total_workouts,
        "current_weight": last_weight,
        "message": "Keep up the good work!"
    }

def alert_missing_workouts(user):
    """
    Checks if user has no logs for the past 3 days.
    """
    cutoff = date.today() - timedelta(days=3)
    logs = ProgressLog.objects.filter(user=user, date__gte=cutoff)
    return not logs.exists()
