import os

import psycopg2 as p
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters

import constants

register_matplotlib_converters()

conn = p.connect(host=os.getenv('POSTGRES_HOST', constants.database_url), dbname=os.getenv('POSTGRES_DB', constants.database_name), user=os.getenv('POSTGRES_USER', constants.database_user), password=os.getenv('POSTGRES_PASSWORD', constants.database_password))
cur = conn.cursor()

# 1 Graph
fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (12,6))

# Has no due connections
cur.execute("""
WITH FinalConversions AS (
    WITH countMarkFinalPerDay AS (
        WITH OpenAppEventDay AS (
            SELECT "createdAt", "memberID", "numberOfDueConnections"
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN "OpenAppTypeContext" ON "Event"."id" = "OpenAppTypeContext"."eventID"
            WHERE name='Open App' AND "OpenAppTypeContext"."numberOfDueConnections">0
        )
        SELECT OpenAppEventDay."createdAt"::DATE AS "date",
            (SELECT CASE WHEN COUNT(*)>0 THEN 1 ELSE 0 END
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" LEFT JOIN "UpdateConnectionTypeContext" ON "Event"."id"="UpdateConnectionTypeContext"."eventID"
            WHERE OpenAppEventDay."memberID" = "Event"."memberID" AND name='Update Connection' AND action='mark as contacted' AND "numberOfDueConnections"=0 AND "Event"."createdAt" BETWEEN OpenAppEventDay."createdAt" AND OpenAppEventDay."createdAt" + '1 hour'::INTERVAL
            ) AS countMarkAsContact1HourNoDue
        FROM OpenAppEventDay
        ORDER BY 1
    )
    SELECT date, SUM(countMarkAsContact1HourNoDue) AS totalEvents, COUNT(*) AS totalMembers
    FROM countMarkFinalPerDay
    GROUP BY 1
    ORDER BY 1
),
AllDates AS (
    SELECT generate_series(MIN("createdAt")::DATE, now()::DATE, INTERVAL '1 day') AS someday
    FROM "Event"
),
t1 AS(
SELECT someday::DATE AS "date", CASE WHEN totalEvents IS NOT NULL THEN totalEvents ELSE 0 END AS totalEvents, CASE WHEN totalMembers IS NOT NULL THEN totalMembers ELSE 0 END AS totalMembers
FROM AllDates LEFT JOIN FinalConversions ON AllDates.someday=FinalConversions.date
)
SELECT date,
    CASE WHEN totalmembers>0 THEN totalevents/totalmembers::DECIMAL ELSE 0 END AS oneday,
    CASE WHEN (sum(totalmembers) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))>0 THEN ((sum(totalevents) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))/(sum(totalmembers) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))) ELSE 0 END AS sevendays, 
    CASE WHEN (sum(totalmembers) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))>0 THEN ((sum(totalevents) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))/(sum(totalmembers) OVER (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW))) ELSE 0 END AS thirtydays
FROM t1;
""")

rows = cur.fetchall()

dates = []
numMarks1Day = []
numMarks7Day = []
numMarks30Day = []
for r in rows:
    dates.append(r[0])
    numMarks1Day.append(r[1])
    numMarks7Day.append(r[2])
    numMarks30Day.append(r[3])


# Graph 1 - % of Sessions where Members Achieve Ideal State: Open App (numDueConnections>0) --> Mark as Contacted (numDueConnections=0) per Session
ax.plot(dates, numMarks30Day, label="Last 30 Days")
ax.plot(dates, numMarks7Day, label="Last 7 Days")
ax.plot(dates, numMarks1Day, label="Last 1 day")
ax.set_title("% of Sessions where Members Achieve Ideal State \nOpen App (numDueConnections>0) --> Mark as Contacted (numDueConnections=0) per Session")
ax.legend(loc='lower left')
ax.set(xlabel='Date', ylabel="Avg #")
# Make ticks on occurrences of each month:
ax.xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.grid(color='gray', linestyle='--')


#plt.show()
def saveFile(folderName):
    fileName = '/Ideal State Session Conversion.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()