from django.urls import path,include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('job_images', views.JobImageViewSet,basename="job_images")

urlpatterns=[
    path('jobs/',views.Jobs.as_view(),name='jobs'),

    path('start_job/<int:pk>/',views.AddJobInfoView.as_view(),name='start_job'),
    path('job_break/<int:pk>/',views.BreakJobView.as_view(),name='job_break'),
    path('finish_job/<int:pk>/',views.FinishJobView.as_view(),name='finish_job'),

    path('',include(router.urls),name='job_images'),
]