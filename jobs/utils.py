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
from decimal import Decimal,ROUND_HALF_UP


def load_time(obj: Job):
    # arrived_job = JobImage.objects.filter(
    #     job=obj, action_type=JobImage.ActionType.arrive_job
    # ).first() # TODO: Take from DB/ Job Model
    
    arrived_job_time = obj.arrived_job_time
    
    # if not arrived_job:
    #     return "No Load Time"
    # arrived_job_time = arrived_job.submitted_at if arrived_job else None
    
    arrived_job_time = (
        timezone.localtime(arrived_job_time) if arrived_job_time else None
    )
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
    # arrived_site = JobImage.objects.filter(
    #     job=obj, action_type=JobImage.ActionType.arrive_site
    # ).first()
    
    arrived_site_time = obj.arrived_site_time
    
    # if not arrived_site:
    #     return "No Travel Time"
    # arrived_site_time = arrived_site.submitted_at if arrived_site else None
    
    arrived_site_time = (
        timezone.localtime(arrived_site_time) if arrived_site_time else None
    )
    departed_at = obj.departed_at if obj.departed_at else None

    if arrived_site_time and departed_at:
        travel_time = arrived_site_time - departed_at
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
    # arrived_site = JobImage.objects.filter(
    #     job=obj, action_type=JobImage.ActionType.arrive_site
    # ).first()
    arrived_site_time = obj.arrived_site_time
    # if not arrived_site:
    #     return "No Unload Time"
    # arrived_site_time = arrived_site.submitted_at if arrived_site else None
    arrived_site_time = (
        timezone.localtime(arrived_site_time) if arrived_site_time else None
    )

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


def total_time(date, driver):
    start_check = PrefillChecks.objects.filter(
        date=date, driver=driver, check_type=PrefillChecks.ChecksTypes.start_day
    )
    
    end_check = PrefillChecks.objects.filter(
        date=date, driver=driver, check_type=PrefillChecks.ChecksTypes.finish_day
    )
    
    if start_check.exists() and end_check.exists():
        start_time = start_check.first().created_at
        end_time = end_check.last().created_at
        
        start_time = timezone.localtime(start_time)
        end_time = timezone.localtime(end_time)
        
        print(f"Start Time: {start_time}, End Time: {end_time}")
        
        total_duration = end_time - start_time
        print(total_duration)
        print(total_duration.seconds//3600)
        print((total_duration.seconds//60)%60)
        
        hours = int(total_duration.seconds // 3600)
        minutes = int(total_duration.seconds // 60) % 60
        
        time_display = f"{hours}:{minutes:02}"
        
        break_duration = timedelta()
        jobs = Job.objects.filter(driver=driver, started_at__date=date)
        for job in jobs:
            if job.break_start and job.break_end:
                break_duration += (job.break_end - job.break_start)
        
        break_seconds = break_duration.total_seconds()
        break_hours = int(break_seconds // 3600)
        break_minutes = int((break_seconds // 60) % 60)
        break_display = f"{break_hours}:{break_minutes:02}"
        
        total_minutes = hours * 60 + minutes
        break_minutes_total = break_hours * 60 + break_minutes
        working_minutes = (total_minutes - break_minutes_total)
        
        working_hours = working_minutes // 60
        working_mins = working_minutes % 60
        working_display = f"{working_hours}:{working_mins:02}"
        
        return time_display, working_display, break_display
    
    return "0:00", "0:00", "0:00"

def total_job_time(obj: Job):
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


def break_time(obj: Job):
    break_start = obj.break_start
    break_end = obj.break_end
    if break_start and break_end:
        break_duration = break_end - break_start
        hours, remainder = divmod(break_duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}"
    return "00:00"


def today_total_driver_time(date):
    prefill_start_check = PrefillChecks.objects.filter(
        date=date,
        check_type=PrefillChecks.ChecksTypes.start_day,
    ).order_by("created_at").first()

    prefill_end_check = PrefillChecks.objects.filter(
        date=date,
        check_type=PrefillChecks.ChecksTypes.finish_day,
    ).order_by("created_at").first()
   
    if prefill_start_check:
        start_time = timezone.localtime(prefill_start_check.created_at)

        if prefill_end_check:
            end_time = timezone.localtime(prefill_end_check.created_at)
        else:
            end_time = timezone.localtime(timezone.now())

        total_duration = end_time - start_time
        hours, remainder = divmod(total_duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}"

    return "00:00"