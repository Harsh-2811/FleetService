from rest_framework.generics import RetrieveAPIView,GenericAPIView
from rest_framework.exceptions import NotFound
from .serializer import *
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from jobs.serializer import *
from jobs.utils import total_job_time,today_total_driver_time,total_time
from decimal import Decimal
from django.utils import timezone
from rest_framework.response import Response

# Create your views here.
class DriverDetails(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DriverSerializer
    
    def get_object(self):
        try:
            return Driver.objects.get(user=self.request.user)
        except Driver.DoesNotExist:
            raise NotFound(detail="Driver not found")

class JobHistory(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = JobHistorySerializer

    
    def get_object(self):
        try:
            return Driver.objects.get(user=self.request.user)
        except Driver.DoesNotExist:
            raise NotFound(detail="Driver not found")
class DriverWork(GenericAPIView): 
    def get(self, request, driver_id):
        try:
            driver = Driver.objects.get(id=driver_id)
        except Driver.DoesNotExist:
            return Response({"detail": "Driver not found."}, status=404)

        today = timezone.now().date()
        today_weekday = today.weekday() 
        current_monday = today - timedelta(days=today_weekday)
    
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        included_days = weekdays[:today_weekday + 1]  
    
        daily_working = {day: "0:00" for day in included_days}
        daily_break = {day: "0:00" for day in included_days}
        daily_total = {day: "0:00" for day in included_days}

        for i in range(today_weekday + 1):
            current_date = current_monday + timedelta(days=i)
            day_name = weekdays[i]
            
            total_hours, working_hours, break_hours = total_time(current_date, driver)
            
            daily_total[day_name] = total_hours
            daily_working[day_name] = working_hours
            daily_break[day_name] = break_hours
        
        today_total, today_working, today_break = total_time(today, driver)
        
        return Response({
            "current_week": {
                "working_hours": daily_working,
                "break_hours": daily_break,
                "total_hours": daily_total,
                "total_working": self.sum_times(daily_working),
                "total_break": self.sum_times(daily_break),
                "total_time": self.sum_times(daily_total)
            },
            "today": {
                "working_hours": today_working,
                "break_hours": today_break,
                "total_hours": today_total
            }
        })
    
    def sum_times(self, time_dict):
        total_seconds = 0
        for time_str in time_dict.values():
            hours, minutes = map(int, time_str.split(":"))
            total_seconds += (hours * 3600) + (minutes * 60)
        
        total_hours = total_seconds // 3600
        total_minutes = (total_seconds % 3600) // 60
        
        return f"{total_hours}:{total_minutes:02}"