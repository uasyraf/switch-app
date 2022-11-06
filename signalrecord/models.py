from django.db import models

# Create your models here.
class Switch(models.Model):
    name = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name

class PingStatusClean(models.Model):
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE)
    state = models.IntegerField()
    date_n_time = models.DateTimeField()

    def __str__(self):
        return str(self.state) + "-" + str(self.date_n_time)

class PingStatusRaw(models.Model):
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE)
    terminal_1 = models.IntegerField()
    terminal_2 = models.IntegerField()
    terminal_3 = models.IntegerField()
    terminal_4 = models.IntegerField()
    terminal_5 = models.IntegerField()
    date_n_time = models.DateTimeField()

    def __str__(self):
        return str(self.date_n_time)

class AlertReport(models.Model):
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=30)
    alert_datetime = models.DateTimeField()
    alert_notification_datetime = models.DateTimeField()

    def __str__(self):
        return str(self.alert_datetime)

class DatabaseStatus(models.Model):
    raw = models.BooleanField()
    parsed = models.BooleanField()

    def __str__(self):
        return "raw: " + str(self.raw) + "\n" + "parsed: " + str(self.parsed)

