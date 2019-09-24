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

# 2 Graphs
fig, ax = plt.subplots(nrows=2, ncols=1, figsize = (12,6))

# Graph 1 - Total Create Connection "hasConnectionImage" Breakdown

cur.execute("""
SELECT COUNT(*) FILTER (WHERE hasConnectionImage=TRUE) AS connectionImages,
    COUNT(*) FILTER (WHERE hasConnectionImage=FALSE) AS noConnectionImages
FROM createConnectionTypeContext """)
rows = cur.fetchall()

totalDue = rows[0][0]
totalNoDue = rows[0][1]

labels='Has Connection Image', 'No Connection Image'

ax[0].pie([totalDue, totalNoDue], labels=labels, autopct='%1.1f%%')
ax[0].set_title("% Breakdown of Create Connection: Has Connection Image vs. No Connection Image TOTAL")
ax[0].axis('equal')


# Graph 2 - Last 30 Days Create Connection "hasConnectionImage" Breakdown
cur.execute("""
WITH dau AS (
  SELECT createdAt::DATE AS "date"
  FROM Event JOIN CreateConnectionTypeContext ON Event.id=CreateConnectionTypeContext.eventID
  GROUP BY 1
  ORDER BY 1
)
SELECT "date",
            (SELECT count(*) FILTER (WHERE hasConnectionImage=TRUE)
            FROM Event JOIN CreateConnectionTypeContext ON Event.id=CreateConnectionTypeContext.eventID
            WHERE Event.createdAt::DATE BETWEEN dau.date - 29 AND dau.date) 
            AS connectionImages,
            (SELECT count(*) FILTER (WHERE hasConnectionImage=FALSE)
            FROM Event JOIN CreateConnectionTypeContext ON Event.id=CreateConnectionTypeContext.eventID
            WHERE Event.createdAt::DATE BETWEEN dau.date - 29 AND dau.date) 
            AS noConnectionImages
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

x = range(1, len(rows)+1)
data = pd.DataFrame({'Percent with image': npe, 'Percent without image': npd, }, index=x)
data_perc = data.divide(data.sum(axis=1), axis=0)
ax[1].stackplot(dates, data_perc['Percent with image'], data_perc['Percent without image'], labels=['Has Image', 'No Image'])
ax[1].set_title("% Breakdown of Create Connection: Has Connection Image vs. No Connection Image by MAUs")
ax[1].legend(loc='lower left')
ax[1].set(xlabel='Date (by Day)', ylabel='%')
# Make ticks on occurrences of each month:
ax[1].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[1].set_yticks(np.arange(0.0, 1.1, 0.1))
ax[1].grid(color='gray', linestyle='--')


#plt.show()
def saveFile(folderName):
    fileName = '/Create Connection Breakdown by Has Connection Image True:False.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()