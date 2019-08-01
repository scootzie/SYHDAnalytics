import psycopg2 as p
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.ticker import MultipleLocator

conn = p.connect(dbname='teamx', user='postgres', password='')
cur = conn.cursor()

# 2 Graphs
fig, ax = plt.subplots(nrows=2, ncols=1)

# Graph 1 - Total Open App numOfDueConnections Breakdown

cur.execute("""
SELECT COUNT(*) FILTER (WHERE numOfDueConnections>0) AS dueConnectionsCount,
    COUNT(*) FILTER (WHERE numOfDueConnections=0) AS noDueConnectionsCount
FROM OpenAppTypeContext
""")
rows = cur.fetchall()

totalDue = rows[0][0]
totalNoDue = rows[0][1]

labels='Due Connections', 'No Due Connections'

ax[0].pie([totalDue, totalNoDue], labels=labels, autopct='%1.1f%%')
ax[0].set_title("% Breakdown of Open App: Due Connections vs. No Due Connections TOTAL")
ax[0].axis('equal')


# Graph 2 - Last 30 Days Open App numOfDueConnections Breakdown
cur.execute("""
WITH dau AS (
  SELECT createdAt::DATE AS "date"
  FROM Event JOIN OpenAppTypeContext ON Event.id=OpenAppTypeContext.eventID
  GROUP BY 1
  ORDER BY 1
)
SELECT "date",
            (SELECT count(DISTINCT memberid) FILTER (WHERE numOfDueConnections>0)
            FROM Event JOIN OpenAppTypeContext ON Event.id=OpenAppTypeContext.eventID
            WHERE Event.createdAt::DATE BETWEEN dau.date - 29 AND dau.date) 
            AS dueConnectionsCount,
            (SELECT count(DISTINCT memberid) FILTER (WHERE numOfDueConnections=0)
            FROM Event JOIN OpenAppTypeContext ON Event.id=OpenAppTypeContext.eventID
            WHERE Event.createdAt::DATE BETWEEN dau.date - 29 AND dau.date) 
            AS noDueConnectionsCount
FROM dau
""")
rows = cur.fetchall()

dates = []
npe = []
npd = []
for r in rows:
    dates.append(r[0])
    npe.append(r[1])
    npd.append(r[2])

x = range(1, len(rows)+1)
data = pd.DataFrame({'Percent Enabled': npe, 'Percent NOT Enabled': npd, }, index=x)
data_perc = data.divide(data.sum(axis=1), axis=0)
ax[1].stackplot(dates, data_perc['Percent Enabled'], data_perc['Percent NOT Enabled'], labels=['Due Connections', 'No Due Connections'])
ax[1].set_title("% Breakdown of Open App: Due Connections vs. No Due Connections by MAUs")
ax[1].legend(loc='lower left')
ax[1].set(xlabel='Date (by Day)', ylabel='%')
# Make ticks on occurrences of each month:
ax[1].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[1].set_yticks(np.arange(0.0, 1.1, 0.1))
ax[1].grid(color='gray', linestyle='--')


plt.show()

conn.close()