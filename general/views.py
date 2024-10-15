from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serilalizer import *
from .models import *

# Create your views here.
class FormFields(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobFormFieldSerializer
    queryset=JobFormField.objects.all()

class SupportPersons(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SupportPersonSerializer
    queryset=SupportPerson.objects.all()


class ContactUsView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactUsSerializer
    queryset=ContactUs.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)