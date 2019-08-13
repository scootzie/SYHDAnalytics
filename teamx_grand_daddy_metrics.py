import os
from datetime import datetime
import importlib

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%m:%d:%Y %H;%M;%S")

folderName = '/Users/scootzie/Documents/SYHDAnalytics/Metrics Reports/' + dt_string
os.mkdir(folderName)
import teamx_app_usage_retention_demographics
teamx_app_usage_retention_demographics.createSection(folderName)
import teamx_app_store_new_members_member_stats
teamx_app_store_new_members_member_stats.createSection(folderName)
import teamx_notifications_effectiveness
teamx_notifications_effectiveness.createSection(folderName)
import teamx_create_connection_stats
teamx_create_connection_stats.createSection(folderName)
import teamx_contact_and_mark_as_contacted
teamx_contact_and_mark_as_contacted.createSection(folderName)
import teamx_search_connections
teamx_search_connections.createSection(folderName)
import teamx_due_connections_ideal_state
teamx_due_connections_ideal_state.createSection(folderName)
import teamx_reminder_frequency_stats
teamx_reminder_frequency_stats.createSection(folderName)