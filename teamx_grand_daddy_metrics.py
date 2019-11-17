import os
from datetime import datetime


def generate_reports():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%m:%d:%Y %H;%M;%S")

    base_folder = os.getenv('REPORT_FOLDER', './Metrics Reports')

    folder_name = base_folder + "/" + dt_string
    os.mkdir(folder_name)
    import teamx_app_usage_retention_demographics
    teamx_app_usage_retention_demographics.create_section(folder_name)
    import teamx_app_store_new_members_member_stats
    teamx_app_store_new_members_member_stats.create_section(folder_name)
    import teamx_notifications_effectiveness
    teamx_notifications_effectiveness.create_section(folder_name)
    import teamx_create_connection_stats
    teamx_create_connection_stats.create_section(folder_name)
    import teamx_contact_and_mark_as_contacted
    teamx_contact_and_mark_as_contacted.create_section(folder_name)
    import teamx_search_connections
    teamx_search_connections.create_section(folder_name)
    import teamx_due_connections_ideal_state
    teamx_due_connections_ideal_state.create_section(folder_name)
    import teamx_reminder_frequency_stats
    teamx_reminder_frequency_stats.create_section(folder_name)
    return folder_name
