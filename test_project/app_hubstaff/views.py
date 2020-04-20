from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

import requests
import json
import logging
from datetime import datetime, timedelta

from app_hubstaff import services, timesheet

logger = logging.getLogger("%s.%s" % ("hubstaff", __name__))

def index(request, **kwargs):
    user_auth_token = request.session.get('auth_token', None)
    if user_auth_token is None:
        return render(template_name="login.html", request=request, context={})
    
    services.fetch_organisations(user_auth_token)
    yesterday =  datetime.utcnow() - timedelta(days=1)
    context = {
        'start_date':yesterday.strftime('%Y-%m-%d'),
        'end_date':yesterday.strftime('%Y-%m-%d'),
        'calculated_report':None
    }
    return render(template_name="index.html", request=request, context=context)


def logout(request, **kwargs):
    if 'auth_token' in request.session:
        del request.session['auth_token']
    return redirect(index)


def login(request, **kwargs):
    email = request.POST.get('email')
    password = request.POST.get('password')

    response_json = services.login_hubstaff(email, password)
    if 'error' in response_json and 'Rate limit' in response_json['error']:
        logger.error('Login error - %s' % response_json)
        return HttpResponse('<h1>Rate limit reached for API requests</h1>')
    elif 'error' in response_json or 'user' not in response_json:
        logger.error('Login error - %s' % response_json)
        return HttpResponse('<h1>Unable to authenticate with the given credentials</h1>')
    
    # hardcoding due to rate limit
    request.session['auth_token'] = response_json['user']['auth_token']
    return redirect(index)

def mock_login(request, **kwargs):
    request.session['auth_token'] = settings.HUBSTAFF_AUTH_TOKEN
    return redirect(index)

def timesheet_report(request, **kwargs):
    yesterday =  datetime.utcnow() - timedelta(days=1)
    start_date = request.POST.get('start_date', yesterday.strftime('%Y-%m-%d'))
    end_date = request.POST.get('end_date', yesterday.strftime('%Y-%m-%d'))
    user_auth_token = request.session.get('auth_token', None)
    if user_auth_token is None:
        return render(template_name="login.html", request=request, context={})

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    if start_date > end_date:
        logger.error('Timesheet error - %s' % response_json)
        return HttpResponse('<h1>Start Date needs to be before End Date</h1>')


    successful, error_message, calculated_report = timesheet.calculate_timesheet_report(user_auth_token, start_date, end_date)
    if not successful:
        logger.error('Timesheet error - %s' % error_message)
        return HttpResponse('<h1>%s</h1>' % error_message)

    start_date = start_date.strftime('%Y-%m-%dT00:00:00Z')
    end_date = end_date.strftime('%Y-%m-%dT23:59:59Z')
    context = {
        'start_date':start_date,
        'end_date':end_date,
        'calculated_report':calculated_report,
    }
    return render(template_name="index.html", request=request, context=context)