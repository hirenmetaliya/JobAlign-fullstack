from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JobListing(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=200, blank=True)
    apply_link = models.URLField(max_length=200, blank=True, null=True)  # New field for apply link

    def __str__(self):
        return f"{self.title} at {self.company}"

    class Meta:
        unique_together = ('title', 'company', 'location')

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    max_matches = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.TextField()

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

class JobMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    match_percentage = models.FloatField()
    apply_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.job_position} at {self.company} - {self.match_percentage}% match"