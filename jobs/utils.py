import io
import os
import zipfile
from django.urls import path
from django.http import HttpResponse
from django.contrib import admin
from .models import *
from rangefilter.filters import (
    DateRangeFilterBuilder,
)
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta



def load_time(obj: Job):
        arrived_job = JobImage.objects.filter(job=obj, action_type=JobImage.ActionType.arrive_job).first()
        if not arrived_job:
            return "No Load Time"
        arrived_job_time = arrived_job.submitted_at if arrived_job else None
        arrived_job_time = timezone.localtime(arrived_job_time) if arrived_job_time else None
        departed_at = obj.departed_at if obj.departed_at else None

       
        if arrived_job_time and departed_at:
            load_time = departed_at - arrived_job_time
            break_start = obj.break_start
            break_end = obj.break_end
            
            if break_start and break_end:
                break_start = timezone.localtime(break_start)
                break_end = timezone.localtime(break_end)
                overlap_start = max(arrived_job_time, break_start)
                overlap_end = min(departed_at, break_end)
                
                if overlap_start < overlap_end:
                    overlap = overlap_end - overlap_start
                    load_time -= overlap

            hours, remainder = divmod(load_time.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}"
        return "No Load Time"
    # load_time.short_description = 'Load Time'
    
def travel_time(obj: Job):
        arrived_site = JobImage.objects.filter(job=obj, action_type=JobImage.ActionType.arrive_site).first()
        if not arrived_site:
            return "No Travel Time"
        arrived_site_time = arrived_site.submitted_at if arrived_site else None
        arrived_site_time = timezone.localtime(arrived_site_time) if arrived_site_time else None
        departed_at = obj.departed_at if obj.departed_at else None

        if arrived_site_time and departed_at:
            travel_time =  arrived_site_time - departed_at
            break_start = obj.break_start
            break_end = obj.break_end
     
            if break_start and break_end:
                break_start = timezone.localtime(break_start)
                break_end = timezone.localtime(break_end)
                overlap_start = max(departed_at, break_start)
                overlap_end = min(arrived_site_time, break_end)
                
                if overlap_start < overlap_end:
                    overlap = overlap_end - overlap_start
                    travel_time -= overlap

            hours, remainder = divmod(travel_time.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}"
        return "No Travel Time"
    
    # travel_time.short_description = 'Travel Time'
    
def unload_time(obj: Job):
        finished_at = obj.finished_at if obj.finished_at else None
        arrived_site = JobImage.objects.filter(job=obj, action_type=JobImage.ActionType.arrive_site).first()
        if not arrived_site:
            return "No Unload Time"
        arrived_site_time = arrived_site.submitted_at if arrived_site else None
        arrived_site_time = timezone.localtime(arrived_site_time) if arrived_site_time else None
     
        if finished_at and arrived_site_time:
            unload_time = finished_at - arrived_site_time
            break_start = obj.break_start
            break_end = obj.break_end
            
            if break_start and break_end:
                break_start = timezone.localtime(break_start)
                break_end = timezone.localtime(break_end)
                overlap_start = max(arrived_site_time, break_start)
                overlap_end = min(finished_at, break_end)
                
                if overlap_start < overlap_end:
                    overlap = overlap_end - overlap_start
                    unload_time -= overlap
            hours, remainder = divmod(unload_time.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}"
        return "No Unload Time"
    
    # unload_time.short_description = 'Unload Time'
    
    
def total_time(obj: Job):
      
        def parse_time(time_str):
            try:
                hours, minutes = map(int, time_str.split(":"))
                return timedelta(hours=hours, minutes=minutes)
            except:
                return timedelta()

        load = load_time(obj)
        travel = travel_time(obj)
        unload = unload_time(obj)

        if not all([load, travel, unload]):
            return "N/A"

        total = parse_time(load) + parse_time(travel) + parse_time(unload)
        total_minutes = total.total_seconds() // 60
        hours, minutes = divmod(total_minutes, 60)
        return f"{int(hours):02}:{int(minutes):02}"
    
    # total_time.short_description = "Total Time"
    
