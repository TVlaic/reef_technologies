from django.conf import settings

import requests
import json
from datetime import datetime, tzinfo

def login_hubstaff(email, password):
    auth_url = settings.HUBSTAFF_ENDPOINT + '/auth'
    header_dict = {
        'App-Token' : settings.HUBSTAFF_APP_TOKEN
    }
    payload = {
        'email' : email,
        'password' : password
    }
    response_json = json.loads(requests.post(auth_url, headers=header_dict, json=payload).text)
    return response_json

def fetch_organisations(auth_token):
    organisation_url = settings.HUBSTAFF_ENDPOINT + '/organizations'
    header_dict = {
        'App-Token' : settings.HUBSTAFF_APP_TOKEN,
        'Auth-Token' : auth_token
    }
    response_json = json.loads(requests.get(organisation_url, headers=header_dict).text)
    return response_json

def fetch_target_organisation_projects(auth_token, target_organisation_id):
    organization_url = settings.HUBSTAFF_ENDPOINT + '/organizations/%d/projects' % target_organisation_id
    header_dict = {
        'App-Token' : settings.HUBSTAFF_APP_TOKEN,
        'Auth-Token' : auth_token
    }
    response_json = json.loads(requests.get(organization_url, headers=header_dict).text)
    return response_json

def fetch_target_organisation_members(auth_token, target_organisation_id):
    organization_url = settings.HUBSTAFF_ENDPOINT + '/organizations/%d/members' % target_organisation_id
    header_dict = {
        'App-Token' : settings.HUBSTAFF_APP_TOKEN,
        'Auth-Token' : auth_token
    }
    response_json = json.loads(requests.get(organization_url, headers=header_dict).text)
    return response_json

def fetch_target_organisation_activities(auth_token, target_organisation_id, 
                                         start_time, end_time):

                            
    
    start_date = start_time.strftime('%Y-%m-%dT00:00:00Z')
    end_date = end_time.strftime('%Y-%m-%dT23:59:00Z')
    activities_url = settings.HUBSTAFF_ENDPOINT + '/activities'
    header_dict = {
        'App-Token' : settings.HUBSTAFF_APP_TOKEN,
        'Auth-Token' : auth_token
    }
    params = {
        'organisations' : [target_organisation_id],
        'start_time' : start_date,
        'stop_time' : end_date,
    }
    
    response_json = json.loads(requests.get(activities_url, params=params, headers=header_dict).text)
    return response_json
    