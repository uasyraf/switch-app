from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.mail import send_mail

from .models import PingStatusClean, PingStatusRaw, Switch, DatabaseStatus, AlertReport
from .constant_app import *
from datetime import datetime
import plotly.express as px

# Create your views here.

def index(request):
    response = redirect('/cleandata')
    return response

def cleandata(request):
    # Filter raw data that was added recently based on last entry datetime in clean data
    try:
        f = PingStatusClean.objects.latest('date_n_time')
    except PingStatusClean.DoesNotExist:
        raise Http404("No PingStatusClean matches the given query.")

    try:
        recent_raws = PingStatusRaw.objects.filter(date_n_time__gt=f.date_n_time)
    except PingStatusRaw.DoesNotExist:
        raise Http404("No PingStatusRaw matches the given query.") 

    # Loop it and add any raw data that is not in the clean data
    for a in recent_raws:
        q = PingStatusClean.objects.filter(Q(switch=a.switch) & Q(date_n_time=a.date_n_time))
        if not q:
            state = a.terminal_1 or a.terminal_2 or a.terminal_3 or a.terminal_4 or a.terminal_5
            b = PingStatusClean(switch=a.switch, state=state, date_n_time=a.date_n_time)
            b.save()

            if not state:
                n = datetime.now()
                c = AlertReport(switch=a.switch, alert_type=ALERT_TYP, alert_datetime=a.date_n_time, alert_notification_datetime=n)
                c.save()

    statechart_1 = gnr8_statechart(SW_1)
    statechart_2 = gnr8_statechart(SW_2)
    statechart_3 = gnr8_statechart(SW_3)

    context = {
        'page_title': 'Clean Data',
        'statechart_1': statechart_1,
        'statechart_2': statechart_2,
        'statechart_3': statechart_3,
    }

    return render(request, 'signalrecord/cleandata.html', context)

def rawdata(request):
    try:
        all_raw_data = PingStatusRaw.objects.all()[::-1]
    except PingStatusRaw.DoesNotExist:
        raise Http404("No PingStatusRaw matches the given query.")
    
    context = {
        'page_title': 'Raw Data',
        'all_raw_data': all_raw_data,
    }

    return render(request, 'signalrecord/rawdata.html', context)

def reports(request):
    try:
        all_reports = AlertReport.objects.all()[::-1]   
    except AlertReport.DoesNotExist:
        raise Http404("No AlertReport matches the given query.")

    context = {
        'page_title': 'Reports',
        'all_reports': all_reports,
    }
    
    return render(request, 'signalrecord/reports.html', context)


# Utility functions
def gnr8_statechart(sw):
    sw_obj = Switch.objects
    psc_obj = PingStatusClean.objects

    if sw == SW_1:
        data = psc_obj.filter(switch=sw_obj.get(name=SW_1))
    elif sw == SW_2:
        data = psc_obj.filter(switch=sw_obj.get(name=SW_2))
    elif sw == SW_3:
        data = psc_obj.filter(switch=sw_obj.get(name=SW_3))
    else:
        raise "Logic for %s does not exist."%str(sw)

    fig = px.line(
        x=[a.date_n_time for a in data],
        y=[a.state for a in data],
        color_discrete_sequence = ['rgb(255,193,69)'],
    )

    statechart = fig.to_html()

    return statechart