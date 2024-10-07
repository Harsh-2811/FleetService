from django.urls import path
from . import views

urlpatterns=[
    path('start_job/',views.StartJob.as_view(),name='start_job'),
    path('jobs/',views.Jobs.as_view(),name='jobs'),
]