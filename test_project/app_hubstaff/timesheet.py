from django.conf import settings
import pandas as pd
import numpy as np

from app_hubstaff import services

def calculate_timesheet_report(user_auth_token, start_date, end_date):
    successful = True
    error_message = ''
    calculated_report = None

    organisations = services.fetch_organisations(user_auth_token)
    if 'organizations' not in organisations:
        successful = False
        error_message = 'Error fetching organisations please try again'
        return successful, error_message, None
    

    my_org_name = settings.TARGET_ORGANIZATION
    my_org_data = None
    for organisation in organisations['organizations']:
        if organisation['name'] == my_org_name:
            my_org_data = organisation
            break

    if my_org_data is None:
        successful = False
        error_message = 'You are not a member of %s organisation' % my_org_name
        return successful, error_message, None
    
    my_org_projects = services.fetch_target_organisation_projects(user_auth_token, int(my_org_data['id']))
    if 'error' in my_org_projects:
        successful = False
        error_message = 'Error fetching projects for organisation'
        return successful, error_message, None

    my_org_members = services.fetch_target_organisation_members(user_auth_token, int(my_org_data['id']))
    if 'error' in my_org_members:
        successful = False
        error_message = 'Error fetching members for organisation'
        return successful, error_message, None

    my_org_activities = services.fetch_target_organisation_activities(user_auth_token, int(my_org_data['id']), start_date, end_date)
    if 'error' in my_org_activities:
        successful = False
        error_message = 'Error fetching activities for organisation'
        if my_org_activities['error'] == 'Date range can not be more than 7 days':
            error_message += " - date range can't be more than 7 days"
        return successful, error_message, None
    
    try:
        user_name_mapper = {
            member['id'] : member['name'] for member in my_org_members['users']
        }

        project_name_mapper = {
            project['id'] : project['name'] for project in my_org_projects['projects']
        }

        df = pd.DataFrame(my_org_activities['activities'])
        df['user'] = df.user_id.apply(lambda x: user_name_mapper.get(x, 'Unknown'))
        df['Project'] = df.project_id.apply(lambda x: project_name_mapper.get(x, 'Unknown'))
        df['tracked'] = df['tracked']/3600
        calculated_report = pd.pivot_table(df, values='tracked', index=['Project'],
                        columns=['user'], aggfunc=np.sum).reset_index()
        calculated_report.iloc[:, 1:] = round(calculated_report.iloc[:, 1:],2).astype(str)
        calculated_report.iloc[:, 1:] = calculated_report.iloc[:, 1:] + 'h'
    except:
        calculated_report = pd.DataFrame(['-'], columns=['Projects'])

    return successful, error_message, calculated_report