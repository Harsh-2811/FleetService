from django.urls import path
from . import views

urlpatterns=[
    path('',views.FormFields.as_view(),name="form_fields"),
]