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
    path("prefill_checks/",views.PrefillChecksView.as_view(),name="prefill_checks"),
    path("is_prefill_checked/",views.IsPrefillCheckedView.as_view(),name="is_prefill_checked"),
    path("start_job/v2/",views.StartJobView.as_view(),name="start_job_v2"),
    path("is_pdf_filled/<int:job_id>/", views.isPDFFilled.as_view(), name="is_pdf_filled"),
    path("fill_pdf/<int:pk>/", views.FillPDF.as_view(), name="fill_pdf"),
    path("update_arrival_time/", views.UpdateArrivalTimeAPI.as_view(), name="update_arrival_time"),
    path("get_arrival_timel/<int:job_id>", views.GetJobArrivalTimesAPI.as_view(), name="get_arrival_time")
]