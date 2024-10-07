from django.urls import path
from . import views

urlpatterns=[
    path('',views.StartJob.as_view(),name='start_job'),
]