from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serilalizer import *
from .models import *

# Create your views here.
class FormFields(ListAPIView):
    serializer_class = JobFormFieldSerializer
    queryset=JobFormField.objects.all()
