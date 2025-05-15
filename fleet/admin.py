from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from decimal import Decimal, ROUND_HALF_UP
from .models import Driver, Vehicle
from jobs.models import Job
from datetime import datetime
from jobs.utils import total_time, total_job_time


class DriverAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "driver_id",
        "license_number",
        "contact_number",
    ]

    search_fields = [
        "user__first_name",
        "user__last_name",
    ]

    readonly_fields = [
        "weekly_hours_breakdown",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": ("user", "license_number", "contact_number"),
            },
        ),
        (
            "Hours Worked",
            {
                "fields": ("weekly_hours_breakdown",),
                "classes": ("collapse",),
            },
        ),
    )

    def weekly_hours_breakdown(self, obj):
        today = timezone.now().date()
        current_monday = today - timedelta(days=today.weekday())

        week3_start = current_monday
        week2_start = week3_start - timedelta(weeks=1)
        week1_start = week3_start - timedelta(weeks=2)

        week1_end = week1_start + timedelta(days=6)
        week2_end = week2_start + timedelta(days=6)
        week3_end = week3_start + timedelta(days=6)

        weeks = [
            (week1_start, week1_end),
            (week2_start, week2_end),
            (week3_start, week3_end),
        ]
        for i in range(3):
            week_start, week_end = weeks[i]
            jobs = Job.objects.filter(
                driver=obj,
                started_at__date__gte=week_start,
                started_at__date__lte=week_end,
            )
            print(jobs, "jobs")
            
            daily_hours = {
                "Monday": "0:00",
                "Tuesday": "0:00",
                "Wednesday": "0:00",
                "Thursday": "0:00",
                "Friday": "0:00",
                "Saturday": "0:00",
                "Sunday": "0:00",
            }
            break_hours = {
                "Monday": "0:00",
                "Tuesday": "0:00",
                "Wednesday": "0:00",
                "Thursday": "0:00",
                "Friday": "0:00",
                "Saturday": "0:00",
                "Sunday": "0:00",
            }
            total_time_hour = {
                "Monday": "0:00",
                "Tuesday": "0:00",
                "Wednesday": "0:00",
                "Thursday": "0:00",
                "Friday": "0:00",
                "Saturday": "0:00",
                "Sunday": "0:00",
            }
        
            for j in range(7):
                day = week_start + timedelta(days=j)
                day_name = day.strftime("%A")
            
                time_display, working_display, break_display = total_time(day, obj)
                
                total_time_hour[day_name] = time_display
                daily_hours[day_name] = working_display
                break_hours[day_name] = break_display
                print(total_time_hour[day_name])
                
            weeks[i] = (week_start, week_end, daily_hours, break_hours, total_time_hour)

        html = '<div style="font-family: Arial; margin-top: 10px;">'
        for week_start, week_end, daily_hours, break_hours, total_time_hour in weeks:
            week_start_str = week_start.strftime("%b %d")
            week_end_str = week_end.strftime("%b %d")
            html += f"<h3>Week ({week_start_str} - {week_end_str})</h3>"
            html += '<table style="border-collapse: collapse; width: 60%;">'
            html += '<tr><th style="border: 1px solid #ccc; padding: 6px;">Day</th><th style="border: 1px solid #ccc; padding: 6px;">Working Hours</th><th style="border: 1px solid #ccc; padding: 6px;">Break Hours</th><th style="border: 1px solid #ccc; padding: 6px;">Total Time</th></tr>'
            
            def time_to_minutes(time_str):
                if ":" in time_str:
                    hours, minutes = time_str.split(":")
                    return int(hours) * 60 + int(minutes)
                return 0
            
            def minutes_to_time(minutes):
                hours = minutes // 60
                mins = minutes % 60
                return f"{hours}:{mins:02}"
            
            total_working_minutes = 0
            total_break_minutes = 0
            total_time_minutes = 0
            
            for day in daily_hours:
                html += f'<tr><td style="border: 1px solid #ccc; padding: 6px;">{day}</td><td style="border: 1px solid #ccc; padding: 6px;">{daily_hours[day]}</td><td style="border: 1px solid #ccc; padding: 6px;">{break_hours[day]}</td><td style="border: 1px solid #ccc; padding: 6px;">{total_time_hour[day]}</td></tr>'
                
 
                total_working_minutes += time_to_minutes(daily_hours[day])
                total_break_minutes += time_to_minutes(break_hours[day])
                total_time_minutes += time_to_minutes(total_time_hour[day])
            
   
            total_working_time = minutes_to_time(total_working_minutes)
            total_break_time = minutes_to_time(total_break_minutes)
            total_time_driver = minutes_to_time(total_time_minutes)
            
            html += f'<tr style="font-weight: bold;"><td style="border: 1px solid #ccc; padding: 6px;">Total</td><td style="border: 1px solid #ccc; padding: 6px;">{total_working_time}</td><td style="border: 1px solid #ccc; padding: 6px;">{total_break_time}</td><td style="border: 1px solid #ccc; padding: 6px;">{total_time_driver}</td></tr>'
            html += "</table><br>"
        html += "</div>"
        return mark_safe(html)

    weekly_hours_breakdown.short_description = "Worked Hours"


admin.site.register(Driver, DriverAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        "plate_number",
        "vehicle_name",
        "vehicle_type",
    ]

    search_fields = [
        "plate_number",
    ]


admin.site.register(Vehicle, VehicleAdmin)
