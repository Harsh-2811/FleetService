from django.urls import path
from . import views

urlpatterns=[
    path('',views.FormFields.as_view(),name="form_fields"),
    path('support_persons/',views.SupportPersons.as_view(),name="support_persons"),
]