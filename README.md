# SYHDAnalytics
Analytics Repo for the Cultivator app

**1) DETERMINE PROBLEM TO SOLVE FOR:**

First, we started with asking ourselves: "What information do we want to learn about from our app?". We brainstormed questions and prioritized them here: https://docs.google.com/spreadsheets/d/1nWwQaEZrdU11-wkWwzlee_UGbQmj3DU_rylWFxZOH-A/edit?usp=sharing.

Then, in the 'Data Visualization Breakdown' sheet in the Google Sheets file linked above, we determined what type of visualization(s) we wanted for each metric.

----------------------------------------------------------------

**2) COLLECT AND STORE DATA:**

After, we determined what specific data we want to capture in our analytics in order to visualize the metrics that we want to capture. We designed the database with this information. **The [ER diagram](https://github.com/scootzie/SYHDAnalytics/blob/master/ER%20Diagram.png) can be found in this repo**. Mock data for these tables can be found in the 'Database Design' sheet in the Google Sheets file linked above.

We then mapped out the user interactions to the corresponding analytics data values that we wanted for each action. This assured us that we covered all the use cases we wanted to cover in the app. This data mapping can be found in this Google Doc: https://docs.google.com/document/d/17PhnJm8EooYixnGG27pQEUkdex-_paWT1bLFayNbx0c/edit?usp=sharing.

----------------------------------------------------------------

**3) CLEAN/ORGANIZE DATA + PERFORM DATA ANALYSIS:**

With the database design in place, we wrote out our .py files to query the database and visualize the data.

To see corresponding visualizations of each graph, see the LucidChart here: https://lucid.app/documents/view/e0134f2b-ba76-4be6-889d-902c5478011a

NOTE: The graphs displayed in the LucidChart are using MOCK DATA, and therefore some of them can appear janky.

**Breakdown of the python files:**

1) **The "Grand Daddy" Metrics file: [teamx_grand_daddy_metrics.py](https://github.com/scootzie/SYHDAnalytics/blob/master/teamx_grand_daddy_metrics.py)**. This file imports the parent scripts that call each python file, as well as names the metrics report with the current date and time.
2) **The Parent Scripts**. These files are imported into teamx_grand_daddy_metrics.py. The parent scripts create the subfolders to categorize the metrics charts and they import the .py files responsible for the querying and visualization. 

The Parent Scripts:

- [New User Stats (Downloads + Permissions)](https://github.com/scootzie/SYHDAnalytics/blob/master/teamx_app_store_new_members_member_stats.py)
- [App Usage Stats (Retention + Demographics)](https://github.com/scootzie/SYHDAnalytics/blob/master/teamx_app_usage_retention_demographics.py)
- [Contact Connection Stats](https://github.com/scootzie/SYHDAnalytics/blob/master/teamx_contact_and_mark_as_contacted.py)
- [Create Connection Stats](https://github.com/scootzie/SYHDAnalytics/blob/master/teamx_create_connection_stats.py)
- ["Ideal State" Stats](https://github.com/scootzie/SYHDAnalytics/blob/master/teamx_due_connections_ideal_state.py) ("Ideal State" == user contacted all the connections that are due to be contacted on their dashboard).

3) **The python files**. These are all the files that start with "**teamx_metrics_...**" and they house the actual data visualization and the SQL that is used to access the database. These files are imported by the parent scripts.

NOTE: Each .py file here ends with a letter system (ex: [teamx_metrics_j.py](https://github.com/scootzie/SYHDAnalytics/blob/master/teamx_metrics_j.py)). The letter system in the .py file names corresponds to the graphs shown in the LucidChart link above.

----------------------------------------------------------------

**4) RETRO:**

_If I did this project again, what would I improve on?_

I would utilize the pandas library in python to better clean and organize the data. Currently, the majority of the "cleaning" happens in the SQL queries that we hit the database with. My data visualizations would have been simpler/easier if I used pandas DataFrames.

I also would utilize the seaborn library in python to make the data visualization coding simpler. In this project, I utilized matplotlib for all of the visualizatoin needs, which was fine, but many of the steps that I took with matplotlib would have been solved with a one-liner seaborn method call.
