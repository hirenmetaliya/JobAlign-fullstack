from django.urls import path
from . import views

urlpatterns = [
    path('api/listings/', views.job_listings_api, name='job_listings_api'),
    path('api/match-jobs/', views.MatchJobsView.as_view(), name='match_jobs'),
]