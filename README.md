# SYHDAnalytics
Analytics Repo for SYHD

Breakdown of these files:

1) The "Grand Daddy" metrics file. This is teamx_grand_daddy_metrics.py. This file imported the parent scripts that call each python file. The grand daddy file creates the main metrics directory, which is titled by the current date and time. This folder will contain subfolders created by the parent scripts that categorize the metrics charts.

2) The parent scripts. These are files imported into teamx_grand_daddy_metrics.py and these files are responsible for creating the subfolders to categorize the metrics charts and import the python files that visualize the data. These are all the files that are not the grand daddy file and are not the "teamx_metrics_..." files.

3) The python files. These are all the files that start with "teamx_metrics_..." and they house the actual data visualization and the SQL that is used to access the database. These files are imported by the parent scripts.
