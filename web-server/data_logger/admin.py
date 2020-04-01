from django.contrib import admin
from .models import Location, Device, Probe, Measurement

# Register your models here.

admin.site.register(Location)
admin.site.register(Device)
admin.site.register(Probe)
admin.site.register(Measurement)
