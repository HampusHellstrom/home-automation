from django.contrib import admin
from .models import Sensor, SensorGroup, Measurement

# Register your models here.


# @admin.register(Sensor)
# class SensorAdmin(admin.ModmelAdmin):
#     # list_filter = ["published"]
#     list_display = ["name", "user"]


admin.site.register(Sensor)
admin.site.register(SensorGroup)
admin.site.register(Measurement)
