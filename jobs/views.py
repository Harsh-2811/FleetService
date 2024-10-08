from rest_framework.generics import ListAPIView,UpdateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
import datetime
from .serializer import *
from jobs.models import *
from drf_spectacular.utils import extend_schema,OpenApiSchemaBase

from drf_spectacular.types import OpenApiTypes

from rest_framework.response import Response
import json

# class CustomRequestBodySchema(OpenApiSchema):
#     def __init__(self):
#         super().__init__(
#             type=OpenApiTypes.OBJECT,
#             properties={
#                 "job_info": OpenApiTypes.JSON_PTR,
#                 "job_data": OpenApiTypes.STRING,
#                 "driver": OpenApiTypes.INTEGER,
#             },
#             required=["job_title", "job_data", "driver"],
#         )


# Create your views here.
# class StartJob(UpdateAPIView):
    
    # queryset = Job.objects.all()
    # permission_classes=[IsAuthenticated]
    
    
    # serializer_class=JobInfoRequestSerializer
    # lookup_field = 'pk'

    # http_method_names=['patch']

    # serializer_class=StartJobSerializer
    
    # request_schema = {
    #     'type': OpenApiTypes.JSON_PTR,
    #     'items': {
    #         'type': OpenApiTypes.OBJECT,
    #         'properties': {
    #             'form_field': {'type': OpenApiTypes.INT},
    #             'value': {'type': OpenApiTypes.STR}
    #         },
    #         'required': ['form_field', 'value']
    #     }
    # }

    # @extend_schema(
    #     request=request_schema,  # Specify the request schema
    #     # summary="Start Job",  # Optional: summary of the operation
    #     # description="This is decriptionssssssssss"
    # )

    # def patch(self, request, *args, **kwargs):
    #     return super().patch(request, *args, **kwargs)

class StartJob(GenericAPIView):
    def patch(self,request,pk,*args,**kwargs):
        # print("************************************")
        # print(self.kwargs)
        # print(json.loads(self.request.body))
        data=json.loads(self.request.body)['job_info']

        job=Job.objects.filter(id=pk).first()
        print(job)
        try:
            for d in data:

                exists=JobInfo.objects.get(
                    job=job,
                    form_field=JobFormField.objects.get(id=d['form_field']),
                    value=d['value']
                )
                if exists:
                    return Response({
                        "Error":"The given value is already exists."
                    })
                    
                jobInfos=JobInfo.objects.create(
                    job=job,
                    form_field=JobFormField.objects.get(id=d['form_field']),
                    value=d['value']
                )
                # print("************ JOB INFO CREATE *****************************")
                # print(jobInfos)

            job_info=JobInfo.objects.filter(job=job)
            serializer=JobInfoSerializer(data=job_info,many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
                
            else:
                return Response(serializer.errors)

        except JobInfo.DoesNotExist:
            return Response({
                "Error":"Object Does not exists."
            })

class Jobs(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=JobSerializer
    
    def get_queryset(self):
        try:
            today = datetime.datetime.today()
            return Job.objects.filter(driver__user=self.request.user,created_at__date=today).order_by('created_at').reverse()
        except Driver.DoesNotExist:
            raise NotFound(detail="Jobs are not found created today.")


from rest_framework.views import APIView

class AddJobInfoView(APIView):
    
    def patch(self, request, pk):
        try:
            job = Job.objects.get(id=pk)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'})

        data = request.data.get('job_info', [])

        if not isinstance(data, list):
            return Response({'error': 'job_info should be a list of form_field_id and value pairs'})
        
        errors = []
        
        for entry in data:
            serializer = JobInfoSerializer(data=entry, context={'job': job})
            
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)
        
        if errors:
            return Response({'errors': errors})
        
        return Response({'message': 'Job info successfully added'})