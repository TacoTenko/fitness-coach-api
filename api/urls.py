from django.urls import path
from .views_workout import (
    RecommendWorkout, CalculateCaloriesBurned, TrackExerciseProgress,
    SuggestRestDays, GetStretchingRoutine
)
from .views_nutrition import (
    RecommendDailyCalories, SuggestMealPlan, CalculateMacros,
    FindHealthySnacks, ValidateHydration
)
from .views_progress import (
    PredictGoalAchievement, CalculateWeightLossGain, TrackWeightProgress,
    CompareWorkouts, CheckProgressTrends, ConvertMeasurementUnits
)
from .views_tools import (
    SuggestSupplements, ValidateWorkoutPlan, GenerateFitnessReport, AlertMissingWorkouts
)

urlpatterns = [
    # Workout Tracking & Recommendations
    path('recommend/workout/', RecommendWorkout.as_view(), name='recommend-workout'),
    path('calculate/calories-burned/', CalculateCaloriesBurned.as_view(), name='calculate-calories-burned'),
    path('track/exercise-progress/<int:user_id>/', TrackExerciseProgress.as_view(), name='track-exercise-progress'),
    path('suggest/rest-days/<int:user_id>/', SuggestRestDays.as_view(), name='suggest-rest-days'),
    path('get/stretching-routine/', GetStretchingRoutine.as_view(), name='get-stretching-routine'),

    # Basic Nutrition & Meal Planning
    path('recommend/daily-calories/', RecommendDailyCalories.as_view(), name='recommend-daily-calories'),
    path('suggest/meal-plan/', SuggestMealPlan.as_view(), name='suggest-meal-plan'),
    path('calculate/macros/', CalculateMacros.as_view(), name='calculate-macros'),
    path('find/healthy-snacks/', FindHealthySnacks.as_view(), name='find-healthy-snacks'),
    path('validate/hydration/', ValidateHydration.as_view(), name='validate-hydration'),

    # Fitness Goal & Progress Monitoring
    path('predict/goal-achievement/<int:user_id>/', PredictGoalAchievement.as_view(), name='predict-goal-achievement'),
    path('calculate/weight-loss-gain/', CalculateWeightLossGain.as_view(), name='calculate-weight-loss-gain'),
    path('track/weight-progress/', TrackWeightProgress.as_view(), name='track-weight-progress'),
    path('compare/workouts/', CompareWorkouts.as_view(), name='compare-workouts'),
    path('check/progress-trends/<int:user_id>/', CheckProgressTrends.as_view(), name='check-progress-trends'),
    path('convert/measurement-units/', ConvertMeasurementUnits.as_view(), name='convert-measurement-units'),

    # Additional Fitness Tools
    path('suggest/supplements/', SuggestSupplements.as_view(), name='suggest-supplements'),
    path('validate/workout-plan/', ValidateWorkoutPlan.as_view(), name='validate-workout-plan'),
    path('generate/fitness-report/<int:user_id>/', GenerateFitnessReport.as_view(), name='generate-fitness-report'),
    path('alert/missing-workouts/<int:user_id>/', AlertMissingWorkouts.as_view(), name='alert-missing-workouts'),
]
