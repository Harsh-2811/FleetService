from django.urls import path,include
from .serializer import *
from . import views

from rest_framework.routers import DefaultRouter

router_job_image = DefaultRouter()
router_job_image.register('job_images', views.JobImageViewSet,basename="job_images")

router_start_job = DefaultRouter()
router_start_job.register('job_start', views.AddJobInfoViewSet,basename="job_start")

router_jobs = DefaultRouter()
router_jobs.register('jobs', views.JobsView,basename="jobs")

router_job_break = DefaultRouter()
router_job_break.register('job_break', views.BreakJobView,basename="job_break")

router_job_finish = DefaultRouter()
router_job_finish.register('job_finish', views.FinishJobView,basename="job_finish")

urlpatterns=[
    path('',include(router_jobs.urls),name='jobs'),
    path('',include(router_start_job.urls),name='start_job'),
    path('',include(router_job_break.urls),name='job_break'),
    path('',include(router_job_finish.urls),name='job_finish'),
    path('',include(router_job_image.urls),name='job_images'),
    path("active_job/",views.ActiveJobView.as_view(),name="active_job"),
]