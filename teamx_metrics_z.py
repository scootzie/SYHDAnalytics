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

# 3 Graphs
fig, ax = plt.subplots(nrows=3, ncols=1, figsize = (12, 6))

# Has no due connections
cur.execute("""
WITH FinalAvgs AS (
    WITH AvgMarkPerDay AS (
        WITH OpenAppEventDay AS (
            SELECT "createdAt", "memberID", "numOfDueConnections"
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN "OpenAppTypeContext" ON "Event"."id" = "OpenAppTypeContext"."eventID"
            WHERE name='Open App' AND "OpenAppTypeContext"."numOfDueConnections"=0
        )
        SELECT OpenAppEventDay."createdAt"::DATE AS "date",
            (SELECT COUNT(*)
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
            WHERE OpenAppEventDay."memberID" = "Event"."memberID" AND name='Update Connection' AND action='mark as contacted' AND "Event"."createdAt" BETWEEN OpenAppEventDay."createdAt" AND OpenAppEventDay."createdAt" + '1 hour'::INTERVAL
            ) AS countMarkAsContact1HourNoDue
        FROM OpenAppEventDay
        ORDER BY 1
    )
    SELECT date, SUM(countMarkAsContact1HourNoDue) AS totalEvents, COUNT(*) AS totalMembers
    FROM AvgMarkPerDay
    GROUP BY 1
    ORDER BY 1
),
AllDates AS (
    SELECT generate_series(MIN("createdAt")::DATE, now()::DATE, INTERVAL '1 day') AS someday
    FROM "Event"
),
t1 AS(
SELECT someday::DATE AS "date", CASE WHEN totalEvents IS NOT NULL THEN totalEvents ELSE 0 END AS totalEvents, CASE WHEN totalMembers IS NOT NULL THEN totalMembers ELSE 0 END AS totalMembers
FROM AllDates LEFT JOIN FinalAvgs ON AllDates.someday=FinalAvgs.date
)
SELECT date, 
    CASE WHEN totalmembers>0 THEN totalevents/totalmembers::DECIMAL ELSE 0 END AS oneday,
    CASE WHEN (sum(totalmembers) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))>0 THEN ((sum(totalevents) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))/(sum(totalmembers) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))) ELSE 0 END AS sevendays, 
    CASE WHEN (sum(totalmembers) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))>0 THEN ((sum(totalevents) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))/(sum(totalmembers) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))) ELSE 0 END AS thirtydays
FROM t1;
""")

noDueConsRows = cur.fetchall()

# Has due connections
cur.execute("""
WITH FinalAvgs AS (
    WITH AvgMarkPerDay AS (
        WITH OpenAppEventDay AS (
            SELECT "createdAt", "memberID", "numOfDueConnections"
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN "OpenAppTypeContext" ON "Event"."id" = "OpenAppTypeContext"."eventID"
            WHERE name='Open App' AND "OpenAppTypeContext"."numOfDueConnections">0
        )
        SELECT OpenAppEventDay."createdAt"::DATE AS "date",
            (SELECT COUNT(*)
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
            WHERE OpenAppEventDay."memberID" = "Event"."memberID" AND name='Update Connection' AND action='mark as contacted' AND "Event"."createdAt" BETWEEN OpenAppEventDay."createdAt" AND OpenAppEventDay."createdAt" + '1 hour'::INTERVAL
            ) AS countMarkAsContact1HourNoDue
        FROM OpenAppEventDay
        ORDER BY 1
    )
    SELECT date, SUM(countMarkAsContact1HourNoDue) AS totalEvents, COUNT(*) AS totalMembers
    FROM AvgMarkPerDay
    GROUP BY 1
    ORDER BY 1
),
AllDates AS (
    SELECT generate_series(MIN("createdAt")::DATE, now()::DATE, INTERVAL '1 day') AS someday
    FROM "Event"
),
t1 AS(
SELECT someday::DATE AS "date", CASE WHEN totalEvents IS NOT NULL THEN totalEvents ELSE 0 END AS totalEvents, CASE WHEN totalMembers IS NOT NULL THEN totalMembers ELSE 0 END AS totalMembers
FROM AllDates LEFT JOIN FinalAvgs ON AllDates.someday=FinalAvgs.date
)
SELECT date, 
    CASE WHEN totalmembers>0 THEN totalevents/totalmembers::DECIMAL ELSE 0 END AS oneday,
    CASE WHEN (sum(totalmembers) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))>0 THEN ((sum(totalevents) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))/(sum(totalmembers) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))) ELSE 0 END AS sevendays, 
    CASE WHEN (sum(totalmembers) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))>0 THEN ((sum(totalevents) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))/(sum(totalmembers) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))) ELSE 0 END AS thirtydays
FROM t1;
""")

dueConsRows = cur.fetchall()


dates = []
noDueCons1Day = []
noDueCons7Day = []
noDueCons30Day = []
dueCons1Day = []
dueCons7Day = []
dueCons30Day =[]
for r in noDueConsRows:
    dates.append(r[0])
    noDueCons1Day.append(r[1])
    noDueCons7Day.append(r[2])
    noDueCons30Day.append(r[3])
for r in dueConsRows:
    dueCons1Day.append(r[1])
    dueCons7Day.append(r[2])
    dueCons30Day.append(r[3])

# Graph 1 - Open App --> Average # of Mark as Contacted in 1 hour over last 30 Days
ax[0].plot(dates, dueCons30Day, label="Due Cons")
ax[0].plot(dates, noDueCons30Day, label="No Due Cons")
ax[0].set_title("Open App --> Average # of 'Mark as Contacted' in 1 hour over last 30 Days, by Due Connections True/False")
ax[0].legend(loc='lower left')
ax[0].set(xlabel='Date', ylabel="Avg #")
# Make ticks on occurrences of each month:
ax[0].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[0].grid(color='gray', linestyle='--')


# Graph 2 - Open App --> Average # of Mark as Contacted in 1 hour over last 7 Days
ax[1].plot(dates, dueCons7Day, label="Due Cons")
ax[1].plot(dates, noDueCons7Day, label="No Due Cons")
ax[1].set_title("Open App --> Average # of 'Mark as Contacted' in 1 hour over last 7 Days, by Due Connections True/False")
ax[1].legend(loc='lower left')
ax[1].set(xlabel='Date', ylabel="Avg #")
# Make ticks on occurrences of each month:
ax[1].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[1].grid(color='gray', linestyle='--')

# Graph 3 - Open App --> Average # of Mark as Contacted in 1 hour over last 1 Day
ax[2].plot(dates, dueCons1Day, label="Due Cons")
ax[2].plot(dates, noDueCons1Day, label="No Due Cons")
ax[2].set_title("Open App --> Average # of 'Mark as Contacted' in 1 hour over last 1 Day, by Due Connections True/False")
ax[2].legend(loc='lower left')
ax[2].set(xlabel='Date', ylabel="Avg #")
# Make ticks on occurrences of each month:
ax[2].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[2].grid(color='gray', linestyle='--')


fig.subplots_adjust(hspace=1)

#plt.show()
def saveFile(folderName):
    fileName = '/Avg # of Mark as Contacted per Session by Due Connections True:False.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()