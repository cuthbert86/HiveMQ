# I will need a file a bit like this one when I make a Django app that can recieve and store data.
from ScoplantUserPanel.models import *
import uuid
from django.db import models

# Create your models here.

class AccountDevice(models.Model):
    Username = models.CharField(max_length=64,unique=True)
    Version = models.CharField(max_length=64)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    MQTT_ID = models.CharField(max_length=64)
    MQTT_USERNAME = models.CharField(max_length=64)
    MQTT_PASSWORD = models.CharField(max_length=64)
    MQTT_PUB = models.CharField(max_length=64)
    MQTT_SUB = models.CharField(max_length=64)
    Date = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(default=False,editable=False ,help_text="Warning! Do Not Active This")

    def __str__(self):
        return self.Username


class LogInfo(models.Model):
    # The device username beacus its uniqu
    id_device = models.ForeignKey(AddDeviceInfo, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Date_Log = models.DateField(auto_now=True)
    Time_Log = models.CharField(max_length=10)
    Battery_Log = models.CharField(max_length=3)
    Lux_Log = models.CharField(max_length=10)
    Humidity_Log = models.CharField(max_length=10)
    Temperature_Log = models.CharField(max_length=10)
    SoilMoisture_Log = models.CharField(max_length=10)
    SoilTemperature_Log = models.CharField(max_length=10)
    EC_Log = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id_device}---{self.Date_Log}-{self.Time_Log}"
