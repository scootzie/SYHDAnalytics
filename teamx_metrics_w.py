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

# Graph 1 - % Breakdown (Cumulative) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT (SELECT COUNT(DISTINCT memberID)
        FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
        WHERE action='change reminder frequency') 
        AS "# of users to change reminder freq",
        COUNT(DISTINCT memberID)
        AS "# of users w/ Connections"
FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
WHERE name='Open App';
""")

rows = cur.fetchall()
top = rows[0][0]
total = rows[0][1]
percent = rows[0][0] / rows[0][1]
other = 1-percent
labels='HAS CHANGE REMINDER FREQ', 'HAS NOT CHANGED REMINDER FREQ'

fig, ax = plt.subplots(nrows=2, ncols=2, figsize = (12,6))
ax[0][0].pie([percent, other], labels=labels, autopct='%1.1f%%')
ax[0][0].set_title("% Breakdown (CUMULATIVE) of Members Who Change Reminder Freq")
ax[0][0].axis('equal')



cur.execute("""
WITH openAndChangeFreqMembers1Day AS (
  SELECT createdAt::DATE AS "date", COUNT(DISTINCT memberID) FILTER(WHERE name='Open App') AS openAppCountDay, COUNT(DISTINCT memberID) FILTER(WHERE action='change reminder frequency') AS changeReminderFrequencyMemberCountDay
  FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
  WHERE name='Open App' OR action='change reminder frequency'
  GROUP BY 1 
)
SELECT date, openAppCountDay, changeReminderFrequencyMemberCountDay, 
            (SELECT count(DISTINCT memberID)
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
            WHERE name='Open App' AND createdAt::DATE BETWEEN openAndChangeFreqMembers1Day.date - 7 AND openAndChangeFreqMembers1Day.date) 
            AS openAppCount7Days,
            (SELECT count(DISTINCT memberID)
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
            WHERE action='change reminder frequency' AND createdAt::DATE BETWEEN openAndChangeFreqMembers1Day.date - 7 AND openAndChangeFreqMembers1Day.date) 
            AS changeReminderFrequencyMember7Days,
            (SELECT count(DISTINCT memberID)
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
            WHERE name='Open App' AND createdAt::DATE BETWEEN openAndChangeFreqMembers1Day.date - 29 AND openAndChangeFreqMembers1Day.date) 
            AS openAppCountMonth,
            (SELECT count(DISTINCT memberID)
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
            WHERE action='change reminder frequency' AND createdAt::DATE BETWEEN openAndChangeFreqMembers1Day.date - 29 AND openAndChangeFreqMembers1Day.date) 
            AS changeReminderFrequencyMemberCountMonth
FROM openAndChangeFreqMembers1Day;
""")

rows = cur.fetchall()
dates = []
successDay = []
failureDay = []
successWeek = []
failureWeek = []
successMonth = []
failureMonth =[]
for r in rows:
    dates.append(r[0])
    successDay.append(r[2])
    failureDay.append(r[1]-r[2])
    successWeek.append(r[4])
    failureWeek.append(r[3]-r[4])
    successMonth.append(r[6])
    failureMonth.append(r[5]-r[6])
x = range(1, len(dates)+1)


# Graph 2 - Open App --> Pull Up Tab Bar Funnel (LAST 30 DAYS)
data = pd.DataFrame({'successMonth': successMonth, 'failureMonth': failureMonth, }, index=x)
data_perc = data.divide(data.sum(axis=1), axis=0)
ax[0][1].stackplot(dates, data_perc['successMonth'], data_perc['failureMonth'], labels=['Change RemFreq', 'No Change RemFreq'])
ax[0][1].set_title("[Unique] Open App --> Change Reminder Freq (LAST 30 DAYS)")
ax[0][1].legend(loc='lower left')
ax[0][1].set(xlabel='Date', ylabel='% Conversion')
# Make ticks on occurrences of each month:
ax[0][1].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[0][1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[0][1].set_yticks(np.arange(0.0, 1.1, 0.2))
ax[0][1].grid(color='gray', linestyle='--')


# Graph 3 - Open App --> Pull Up Tab Bar Funnel (LAST 7 DAYS)
data1 = pd.DataFrame({'successWeek': successWeek, 'failureWeek': failureWeek, }, index=x)
data_perc1 = data1.divide(data1.sum(axis=1), axis=0)
ax[1][0].stackplot(dates, data_perc1['successWeek'], data_perc1['failureWeek'], labels=['Change RemFreq', 'No Change RemFreq'])
ax[1][0].set_title("[Unique] Open App --> Change Reminder Freq (LAST 7 DAYS)")
ax[1][0].legend(loc='lower left')
ax[1][0].set(xlabel='Date', ylabel='% Conversion')
# Make ticks on occurrences of each month:
ax[1][0].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[1][0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[1][0].set_yticks(np.arange(0.0, 1.1, 0.2))
ax[1][0].grid(color='gray', linestyle='--')

# Graph 4 - Open App --> Pull Up Tab Bar Funnel (LAST 1 DAY)
data2 = pd.DataFrame({'successDay': successDay, 'failureDay': failureDay, }, index=x)
data_perc2 = data2.divide(data2.sum(axis=1), axis=0)
ax[1][1].stackplot(dates, data_perc2['successDay'], data_perc2['failureDay'], labels=['Change RemFreq', 'No Change RemFreq'])
ax[1][1].set_title("[Unique] Open App --> Change Reminder Freq (LAST 1 DAY)")
ax[1][1].legend(loc='lower left')
ax[1][1].set(xlabel='Date', ylabel='% Conversion')
# Make ticks on occurrences of each month:
ax[1][1].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[1][1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[1][1].set_yticks(np.arange(0.0, 1.1, 0.2))
ax[1][1].grid(color='gray', linestyle='--')


#plt.show()
def saveFile(folderName):
    fileName = '/Members Who Change Reminder Frequencies.pdf'
    plt.savefig(folderName + fileName)
    plt.close()

conn.close()