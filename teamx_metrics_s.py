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

cur.execute("""
WITH openAndSearch1Day AS (
  SELECT createdAt::DATE AS "date", COUNT(*) FILTER(WHERE name='Open App') AS openAppCountDay, COUNT(*) FILTER(WHERE action='use search bar') AS searchCountDay
  FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID
  WHERE name='Open App' OR action='use search bar'
  GROUP BY 1 
)
SELECT date, openAppCountDay, searchCountDay, 
            (SELECT count(*)
            FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID
            WHERE name='Open App' AND createdAt::DATE BETWEEN openAndSearch1Day.date - 7 AND openAndSearch1Day.date) 
            AS openAppCount7Days,
            (SELECT count(*)
            FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID
            WHERE action='use search bar' AND createdAt::DATE BETWEEN openAndSearch1Day.date - 7 AND openAndSearch1Day.date) 
            AS searchCount7Days,
            (SELECT count(memberid)
            FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID
            WHERE name='Open App' AND createdAt::DATE BETWEEN openAndSearch1Day.date - 29 AND openAndSearch1Day.date) 
            AS openAppCountMonth,
            (SELECT count(memberid)
            FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID
            WHERE action='use search bar' AND createdAt::DATE BETWEEN openAndSearch1Day.date - 29 AND openAndSearch1Day.date) 
            AS searchCountMonth
FROM openAndSearch1Day;
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

fig, ax = plt.subplots(nrows=3, ncols=1, figsize = (12,6))

# Graph 1 - Open App --> Use Search Bar Funnel (LAST 30 DAYS)
data = pd.DataFrame({'successMonth': successMonth, 'failureMonth': failureMonth, }, index=x)
data_perc = data.divide(data.sum(axis=1), axis=0)
ax[0].stackplot(dates, data_perc['successMonth'], data_perc['failureMonth'], labels=['Searched', 'Did Not Search'])
ax[0].set_title("Open App --> Use Search Bar Funnel (LAST 30 DAYS)")
ax[0].legend(loc='lower left')
ax[0].set(xlabel='Date', ylabel='% Conversion')
# Make ticks on occurrences of each month:
ax[0].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[0].set_yticks(np.arange(0.0, 1.1, 0.2))
ax[0].grid(color='gray', linestyle='--')


# Graph 2 - Open App --> Use Search Bar Funnel (LAST 7 DAYS)
data1 = pd.DataFrame({'successWeek': successWeek, 'failureWeek': failureWeek, }, index=x)
data_perc1 = data1.divide(data1.sum(axis=1), axis=0)
ax[1].stackplot(dates, data_perc1['successWeek'], data_perc1['failureWeek'], labels=['Searched', 'Did Not Search'])
ax[1].set_title("Open App --> Use Search Bar Funnel (LAST 7 DAYS)")
ax[1].legend(loc='lower left')
ax[1].set(xlabel='Date', ylabel='% Conversion')
# Make ticks on occurrences of each month:
ax[1].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[1].set_yticks(np.arange(0.0, 1.1, 0.2))
ax[1].grid(color='gray', linestyle='--')

# Graph 3 - Open App --> Use Search Bar Funnel (LAST 1 DAY)
data2 = pd.DataFrame({'successDay': successDay, 'failureDay': failureDay, }, index=x)
data_perc2 = data2.divide(data2.sum(axis=1), axis=0)
ax[2].stackplot(dates, data_perc2['successDay'], data_perc2['failureDay'], labels=['Searched', 'Did Not Search'])
ax[2].set_title("Open App --> Use Search Bar Funnel (LAST 1 DAY)")
ax[2].legend(loc='lower left')
ax[2].set(xlabel='Date', ylabel='% Conversion')
# Make ticks on occurrences of each month:
ax[2].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[2].set_yticks(np.arange(0.0, 1.1, 0.2))
ax[2].grid(color='gray', linestyle='--')

plt.tight_layout()
#plt.show()
def saveFile(folderName):
    fileName = '/Open App to Use Search Bar Funnel.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()