from django.urls import path,include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('job_images', views.JobImageViewSet,basename="job_images")

urlpatterns=[
    path('start_job/<int:pk>/',views.AddJobInfoView.as_view(),name='start_job'),
    path('',include(router.urls),name='job_images'),
    path('jobs/',views.Jobs.as_view(),name='jobs'),
]