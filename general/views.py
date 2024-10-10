from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serilalizer import *
from .models import *

# Create your views here.
class FormFields(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobFormFieldSerializer
    queryset=JobFormField.objects.all()
