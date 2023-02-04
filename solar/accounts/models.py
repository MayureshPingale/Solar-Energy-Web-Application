from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


class Solaranalysis(models.Model):
    customer = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    current_day_production = models.CharField(max_length=3000)
    current_day_usage = models.CharField(max_length=300)
    weekly_day_production = models.CharField(max_length=3000)
    weekly_day_usage = models.CharField(max_length=3000)

