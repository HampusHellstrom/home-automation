from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.



class Sensor(models.Model):
    TEMPERATURE = 0
    HUMIDITY = 1
    BRIGHTNESS = 2
    MOISTURE = 3
    RAIN = 4
    UNITS =(
        (TEMPERATURE, "Temperature"),
        (HUMIDITY, "Humidity"),
        (BRIGHTNESS, "Brightness"),
        (MOISTURE, "Moisture"),
        (RAIN, "Rain"),
    )

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="locations")
    description = models.TextField(null=True, blank=True, max_length=500)
    name = models.CharField(max_length=32)
    prop = models.IntegerField(choices = UNITS)

    def __str__(self):
        return f"{self.id}. {self.name} - {self.UNITS[self.prop][1]} ({self.user.username})"


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor,
                              on_delete=models.CASCADE,
                              related_name="measurements")
    datetime = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=16, decimal_places=3)

    def __str__(self):
        return f"{self.datetime}"

    # def save(self, *args, **kwargs):
    #     print(dir(self))
    #     if self.datetime is None:
    #         datetime = datetime.now()
    #     super(Measurement, self).save(*args, **kwargs)


class SensorGroup(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="sensor_groups")
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True, max_length=500)
    sensors = models.ManyToManyField(Sensor)


    class Meta:
        unique_together = (("user", "name"),)
        index_together = (("user", "name"),)

    def __str__(self):
        return f"{self.id}. {self.name} ({self.user.username})"

