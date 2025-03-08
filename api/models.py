from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    height_cm = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    # Additional user-related fields...

    def __str__(self):
        return self.username

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    calories_burned_estimate = models.FloatField()

    def __str__(self):
        return self.name

class ProgressLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    weight_kg = models.FloatField()
    workouts_completed = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} on {self.date}"

class MealPlan(models.Model):
    plan_name = models.CharField(max_length=100)
    description = models.TextField()
    calories = models.PositiveIntegerField()

    def __str__(self):
        return self.plan_name
