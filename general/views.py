from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .serilalizer import *
from .models import *

# Create your views here.
class FormFields(RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = JobFormFieldSerializer

    def get(self,request,*ags,**kwargs):
        fields=JobFormField.objects.all()
        serializer=JobFormFieldSerializer(fields,many=True)
        return Response(serializer.data)