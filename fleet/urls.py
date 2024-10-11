from django.urls import path
from . import views

urlpatterns=[
    path('driver/',views.DriverDetails.as_view(),name="driver"),
    path('driver/job_histories/',views.JobHistory.as_view(),name="job_history"),

]