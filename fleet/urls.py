from django.urls import path
from . import views

urlpatterns=[
    path('driver/',views.DriverDetails.as_view(),name="driver"),
]