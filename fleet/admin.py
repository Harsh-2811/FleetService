from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from decimal import Decimal, ROUND_HALF_UP
from .models import Driver, Vehicle
from jobs.models import Job
from datetime import datetime
from jobs.utils import total_time


class DriverAdmin(admin.ModelAdmin):
    list_display = [
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
            total_hours = Decimal("0.00")
            daily_hours = {
                "Monday": Decimal("0.00"),
                "Tuesday": Decimal("0.00"),
                "Wednesday": Decimal("0.00"),
                "Thursday": Decimal("0.00"),
                "Friday": Decimal("0.00"),
                "Saturday": Decimal("0.00"),
                "Sunday": Decimal("0.00"),
            }
            break_hours = {
                "Monday": Decimal("0.00"),
                "Tuesday": Decimal("0.00"),
                "Wednesday": Decimal("0.00"),
                "Thursday": Decimal("0.00"),
                "Friday": Decimal("0.00"),
                "Saturday": Decimal("0.00"),
                "Sunday": Decimal("0.00"),
            }
            for job in jobs:
                total_hours += Decimal(total_time(job).replace(":", "."))
                job_day = job.started_at.strftime("%A")
                daily_hours[job_day] += Decimal(total_time(job).replace(":", "."))
                if job.break_start and job.break_end:
                    break_duration = job.break_end - job.break_start
                    break_hours[job_day] += Decimal(
                        break_duration.total_seconds() / 3600
                    ).quantize(Decimal("0.01"))
            daily_hours = {
                day: hours.quantize(Decimal("0.01"))
                for day, hours in daily_hours.items()
            }
            total_hours = total_hours.quantize(Decimal("0.01"))
            break_hours = {
                day: hours.quantize(Decimal("0.01"))
                for day, hours in break_hours.items()
            }
            weeks[i] = (week_start, week_end, total_hours, daily_hours, break_hours)

        html = '<div style="font-family: Arial; margin-top: 10px;">'
        for week_start, week_end, total_hours, daily_hours, break_hours in weeks:
            week_start_str = week_start.strftime("%b %d")
            week_end_str = week_end.strftime("%b %d")
            html += f"<h3>Week ({week_start_str} - {week_end_str})</h3>"
            html += '<table style="border-collapse: collapse; width: 60%;">'
            html += '<tr><th style="border: 1px solid #ccc; padding: 6px;">Day</th><th style="border: 1px solid #ccc; padding: 6px;">Working Hours</th><th style="border: 1px solid #ccc; padding: 6px;">Break Hours</th></tr>'
            for day, hours in daily_hours.items():
                html += f'<tr><td style="border: 1px solid #ccc; padding: 6px;">{day}</td><td style="border: 1px solid #ccc; padding: 6px;">{hours}</td><td style="border: 1px solid #ccc; padding: 6px;">{break_hours[day]}</td></tr>'
            html += f'<tr style="font-weight: bold;"><td style="border: 1px solid #ccc; padding: 6px;">Total</td><td style="border: 1px solid #ccc; padding: 6px;">{total_hours}</td><td style="border: 1px solid #ccc; padding: 6px;">{sum(break_hours.values())}</td></tr>'
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
