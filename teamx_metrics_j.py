import os
import psycopg2 as p
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.ticker import MultipleLocator

conn = p.connect(host=os.getenv('POSTGRES_HOST', 'http://127.0.0.1:5432'), dbname=os.getenv('POSTGRES_DB', 'teamx'), user=os.getenv('POSTGRES_USER', 'postgres'), password=os.getenv('POSTGRES_PASSWORD', ''))
cur = conn.cursor()

cur.execute("""
WITH AllMonths AS (
SELECT date_trunc('month', generate_series(MIN("createdAt")::DATE, now()::DATE, INTERVAL '1 month')) AS somemonth
FROM MEMBER
)
SELECT AllMonths.somemonth, COUNT(*) FILTER (WHERE notificationsEnabled=TRUE) AS numNotificationsEnabled, COUNT(*) FILTER (WHERE notificationsEnabled=FALSE) AS numNotificationsDisabled
FROM AllMonths LEFT JOIN MEMBER ON AllMonths.somemonth = date_trunc('month', member."createdAt")
GROUP BY 1
ORDER BY 1
""")

rows = cur.fetchall()

totalEnabled = 0
totalDisabled = 0
dates = []
npe = []
npd = []
for r in rows:
    totalEnabled += r[1]
    totalDisabled += r[2]
    dates.append(r[0])
    npe.append(r[1])
    npd.append(r[2])

labels='ENABLED', 'NOT ENABLED'

# 3 Graphs
fig, ax = plt.subplots(nrows=3, ncols=1, figsize = (10,6))

# Graph 1 - % Notifications Enabled (Cumulative) - Pie Chart
ax[0].pie([totalEnabled, totalDisabled], labels=labels, autopct='%1.1f%%')
ax[0].set_title("% Breakdown of Members Who Enable Notifications")
ax[0].axis('equal')

# Graph 2 - % Notifications Enabled by Month of Created Date - Line Graph
x = range(1, len(rows)+1)
data = pd.DataFrame({'Percent Enabled': npe, 'Percent NOT Enabled': npd, }, index=x)
data_perc = data.divide(data.sum(axis=1), axis=0)
ax[1].stackplot(dates, data_perc['Percent Enabled'], data_perc['Percent NOT Enabled'], labels=['Percent Enabled', 'Percent NOT Enabled'])
ax[1].set_title("Notification Permissions by Month of "Member" Creation")
ax[1].legend(loc='lower left')
ax[1].set(xlabel='Creation Date (Month)', ylabel='% of Members')
# Make ticks on occurrences of each month:
ax[1].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[1].set_yticks(np.arange(0.0, 1.1, 0.1))
ax[1].grid(color='gray', linestyle='--')


cur.execute("""
WITH dau AS (
  SELECT "createdAt"::DATE AS "date", count(DISTINCT memberid) AS dau
  FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
  WHERE name='Open App'
  GROUP BY 1 
)
SELECT "date",
            (SELECT count(DISTINCT memberid) FILTER (WHERE notificationsEnabled=TRUE)
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN MEMBER ON "Event"."memberID"="Member"."id"
            WHERE name='Open App' AND "Event"."createdAt"::DATE BETWEEN dau.date - 29 AND dau.date) 
            AS mauNotificationsEnabledCount,
            (SELECT count(DISTINCT memberid) FILTER (WHERE notificationsEnabled=FALSE)
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN MEMBER ON "Event"."memberID"="Member"."id"
            WHERE name='Open App' AND "Event"."createdAt"::DATE BETWEEN dau.date - 29 AND dau.date) 
            AS mauNotificationsDisabledCount
FROM dau;
""")

rows = cur.fetchall()

dates = []
npe = []
npd = []
for r in rows:
    dates.append(r[0])
    npe.append(r[1])
    npd.append(r[2])


# Graph 3 - % Notifications Enabled by MAUs - Stackplot
x = range(1, len(rows)+1)
data = pd.DataFrame({'Percent Enabled': npe, 'Percent NOT Enabled': npd, }, index=x)
data_perc = data.divide(data.sum(axis=1), axis=0)
ax[2].stackplot(dates, data_perc['Percent Enabled'], data_perc['Percent NOT Enabled'], labels=['Percent Enabled', 'Percent NOT Enabled'])
ax[2].set_title("Notification Permissions Breakdown by MAUs")
ax[2].legend(loc='lower left')
ax[2].set(xlabel='Date (by Day)', ylabel='% of MAUs')
# Make ticks on occurrences of each month:
ax[2].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[2].set_yticks(np.arange(0.0, 1.1, 0.1))
ax[2].grid(color='gray', linestyle='--')


fig.subplots_adjust(hspace=.6)
#plt.show()
def saveFile(folderName):
    fileName = '/Notification Permissions Breakdown.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()
