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

# 1 Graph
fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (12,7))

# Has no due connections
cur.execute("""
WITH FinalAvgs AS (
    WITH createExistsPerSesh AS (
        WITH searchBarEventSesh AS (
            SELECT createdAt, memberID
            FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID
            WHERE name='Search All Connections' AND action='use search bar'
        )
        SELECT searchBarEventSesh.createdAt::DATE AS "date",
            CASE WHEN (SELECT COUNT(*)
            FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID
            WHERE searchBarEventSesh.memberID = Event.memberID AND name='Create Connection' AND Event.createdAt BETWEEN searchBarEventSesh.createdAt AND searchBarEventSesh.createdAt + '1 hour'::INTERVAL
            )>0 THEN 1 ELSE 0 END AS createExists1Hour
        FROM searchBarEventSesh
        ORDER BY 1
    )
    SELECT date, SUM(createExists1Hour) AS totalCreates, COUNT(*) AS totalSearches
    FROM createExistsPerSesh
    GROUP BY 1
    ORDER BY 1
),
AllDates AS (
    SELECT generate_series(MIN(createdAt)::DATE, now()::DATE, INTERVAL '1 day') AS someday
    FROM EVENT
),
t1 AS(
SELECT someday::DATE AS "date", CASE WHEN totalCreates IS NOT NULL THEN totalCreates ELSE 0 END AS totalCreates, CASE WHEN totalSearches IS NOT NULL THEN totalSearches ELSE 0 END AS totalSearches
FROM AllDates LEFT JOIN FinalAvgs ON AllDates.someday=FinalAvgs.date
)
SELECT date,
    CASE WHEN totalSearches>0 THEN totalCreates/totalSearches::DECIMAL ELSE 0 END AS oneday,
    CASE WHEN (sum(totalSearches) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))>0 THEN ((sum(totalCreates) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))/(sum(totalSearches) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))) ELSE 0 END AS sevendays, 
    CASE WHEN (sum(totalSearches) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))>0 THEN ((sum(totalCreates) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))/(sum(totalSearches) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))) ELSE 0 END AS thirtydays
FROM t1
""")

rows = cur.fetchall()

dates = []
num1Day = []
num7Day = []
num30Day = []
for r in rows:
    dates.append(r[0])
    num1Day.append(r[1])
    num7Day.append(r[2])
    num30Day.append(r[3])


# Graph 1 - Mark as Contacted --> Average # of Mark as Contacted per session
ax.plot(dates, num30Day, label="Last 30 Days")
ax.plot(dates, num7Day, label="Last 7 Days")
ax.plot(dates, num1Day, label="Last 1 day")
ax.set_title("Use Search Bar --> Create Connection Within 1 Hour (Conversion)")
ax.legend(loc='lower left')
ax.set(xlabel='Date', ylabel="Conversion %")
# Make ticks on occurrences of each month:
ax.xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.grid(color='gray', linestyle='--')


#plt.show()
def saveFile(folderName):
    fileName = '/Use Search Bar to Create Connection Funnel.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()