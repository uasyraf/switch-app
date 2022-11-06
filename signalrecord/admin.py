from django.contrib import admin
from .models import AlertReport, DatabaseStatus, PingStatusClean, PingStatusRaw, Switch

# Register your models here.
admin.site.register(Switch)
admin.site.register(PingStatusClean)
admin.site.register(PingStatusRaw)
admin.site.register(AlertReport)
admin.site.register(DatabaseStatus)