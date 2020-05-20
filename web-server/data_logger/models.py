from django.db import models
from django.contrib.auth.models import User
from datetime.datetime import now

# Create your models here.

class Location(models.Model):

    class Meta:
        unique_together = (("user", "name"),)
        index_together = (("user", "name"),)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="locations")
    name = models.CharField(max_length=32)


class Device(models.Model):
    location = models.ForeignKey(Location,
                                 on_delete=models.CASCADE,
                                 related_name="devices")
    name = models.CharField(max_length=32)

    class Meta:
        unique_together = (("location", "name"),)
        index_together = (("location", "name"),)

    def __str__(self):
        return f"{self.location.name} - {self.name}"


class Probe(models.Model):
    device = models.ForeignKey(Device,
                               on_delete=models.CASCADE,
                               related_name="probes")
    name = models.CharField(max_length=32)

    class Units(models.IntegerChoices):
        CESLIUS = 1
        HUMIDITY = 2
        LUMEN = 3
        MOISTURE = 4

    unit = models.IntegerField(choices=Units.choices)

    def __str__(self):
        return f"{self.device.location.name} - {self.device.name} - {self.name}"


class Measurement(models.Model):
    probe = models.ForeignKey(Probe,
                              on_delete=models.CASCADE,
                              related_name="measurements")
    datetime = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=16, decimal_places=3)

    def __str__(self):
        return f"{self.datetime}"

    def save(self, *args, **kwargs):
        if datetime is None:
            datetime = now()
        super(MyModel, self).save(*args, **kwargs)
