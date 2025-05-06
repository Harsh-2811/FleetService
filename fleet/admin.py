from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from decimal import Decimal, ROUND_HALF_UP
from .models import Driver, Vehicle
from jobs.models import Job
from datetime import datetime


class DriverAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'driver_id',
        'license_number',
        'contact_number',
    ]

    search_fields = [
        'user__first_name',
        'user__last_name',
    ]

    readonly_fields = [
        'weekly_hours_breakdown',
    ]

    fieldsets = (
        (None, {
            'fields': ('user', 'license_number', 'contact_number'),
        }),
        ('Hours Worked', {
            'fields': ('weekly_hours_breakdown',),
            'classes': ('collapse',),
        }),
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

        breakdown = {
            f"Week 1 ({week1_start.strftime('%b %d')} - {week1_end.strftime('%b %d')})": {day: Decimal('0.00') for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
            f"Week 2 ({week2_start.strftime('%b %d')} - {week2_end.strftime('%b %d')})": {day: Decimal('0.00') for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
            f"Week 3 (This Week: {week3_start.strftime('%b %d')} - {week3_end.strftime('%b %d')})": {day: Decimal('0.00') for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
        }

        jobs = Job.objects.filter(
            driver=obj,
            started_at__date__gte=week1_start,
            started_at__date__lte=week3_end
        )

        for job in jobs:
            if not job.started_at or not job.finished_at:
                continue

            start = job.started_at
            end = job.finished_at

            if job.break_start and job.break_end:
                break_duration = job.break_end - job.break_start
                end -= break_duration

            current = start
            while current < end:
                next_midnight = timezone.make_aware(datetime.combine(current.date() + timedelta(days=1), datetime.min.time()))

                segment_end = min(end, next_midnight)
                seconds = (segment_end - current).total_seconds()
                hours = Decimal(seconds / 3600).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                date = current.date()
                day_name = date.strftime('%A')

                if week1_start <= date <= week1_end:
                    week_key = list(breakdown.keys())[0]
                elif week2_start <= date <= week2_end:
                    week_key = list(breakdown.keys())[1]
                elif week3_start <= date <= week3_end:
                    week_key = list(breakdown.keys())[2]
                else:
                    current = segment_end
                    continue

                breakdown[week_key][day_name] += hours
                current = segment_end

        html = '<div style="font-family: Arial; margin-top: 10px;">'
        for week, days in breakdown.items():
            html += f'<h3>{week}</h3>'
            html += '<table style="border-collapse: collapse; width: 60%;">'
            html += '<tr><th style="border: 1px solid #ccc; padding: 6px;">Day</th><th style="border: 1px solid #ccc; padding: 6px;">Hours</th></tr>'
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                hours = days[day].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                html += f'<tr><td style="border: 1px solid #ccc; padding: 6px;">{day}</td><td style="border: 1px solid #ccc; padding: 6px;">{hours}</td></tr>'
            html += '</table><br>'
        html += '</div>'
        return mark_safe(html)

    weekly_hours_breakdown.short_description = "Worked Hours"

admin.site.register(Driver, DriverAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        'plate_number',
        'vehicle_name',
        'vehicle_type',
    ]

    search_fields = [
        'plate_number',
    ]

admin.site.register(Vehicle, VehicleAdmin)
