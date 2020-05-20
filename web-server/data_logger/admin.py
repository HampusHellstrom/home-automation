from django.contrib import admin
from .models import Location, Device, Probe, Measurement

# Register your models here.


@admin.register(Location)
class LocationAdmin(admin.ModmelAdmin):
    # list_filter = ["published"]
    list_display = ["name", "user"]


# admin.site.register(Location)
admin.site.register(Device)
admin.site.register(Probe)
admin.site.register(Measurement)
