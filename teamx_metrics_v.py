import os

import numpy as np
import psycopg2 as p
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters

import constants

register_matplotlib_converters()
from matplotlib.ticker import MultipleLocator

conn = p.connect(host=os.getenv('POSTGRES_HOST', constants.database_url),
                 dbname=os.getenv('POSTGRES_DB', constants.database_name),
                 user=os.getenv('POSTGRES_USER', constants.database_user),
                 password=os.getenv('POSTGRES_PASSWORD', constants.database_password))
cur = conn.cursor()

fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(16, 6))

# Graph 1 - Histogram of Hour of Day for Open App Events
cur.execute("""
SELECT EXTRACT(isodow from "createdAt") as dayofweek, EXTRACT(HOUR from "createdAt") as hour
FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
WHERE name='Open App';
""")

rows = cur.fetchall()
hours = []
days = []
bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
for r in rows:
    days.append(r[0])
    hours.append(r[1])
xrange = np.arange(0, 25, 3)
hourLabels = ['12AM', '3AM', '6AM', '9AM', '12PM', '3PM', '6PM', '9PM']
ax[0].hist(hours, bins=bins)
ax[0].set_xticks(xrange)
ax[0].xaxis.set_minor_locator(MultipleLocator(1))
ax[0].set_title('Hour of Day for Open App Events')
ax[0].set(xlabel='Hour of Day', ylabel='# of Open App Events')
ax[0].set_xticklabels(hourLabels)

# Graph 2 - Histogram of Day of Week for Open App Events
bins = [1, 2, 3, 4, 5, 6, 7, 8]
xrange1 = np.arange(1, 8, 1)
dayLabels = ['Monday', 'Tuesday', ' Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
ax[1].hist(days, bins=bins)
ax[1].set_xticks(xrange1)
ax[1].xaxis.set_minor_locator(MultipleLocator(1))
ax[1].set_title('Day of the Week for Open App Events')
ax[1].set(xlabel='Day of the Week', ylabel='# of Open App Events')
ax[1].set_xticklabels(dayLabels)

# Graph 3 - Bar Chart of Counts for 'day of week' and 'time of day' for Open App
cur.execute("""
WITH AllDaysAndHours AS (
    WITH AllDays AS (
        SELECT EXTRACT (isodow from generate_series('2019-07-08 00:00:00', '2019-07-14 00:00:00', INTERVAL '1 day')) AS dayofweek
    ),
    AllHours AS (
        SELECT EXTRACT (HOUR from generate_series('2019-07-08 00:00:00', '2019-07-08 23:59:59', INTERVAL '1 hour')) AS hourofday
    )
    SELECT *
    FROM AllDays CROSS JOIN AllHours
    ORDER BY dayofweek, hourofday
),
OpenAppDaysAndTimes AS (
    SELECT EXTRACT(isodow from "createdAt") as dayofweek, EXTRACT(HOUR from "createdAt") as hourofday, COUNT(*) AS numEvents
    FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
    WHERE name='Open App'
    GROUP BY 1, 2
    ORDER BY 1, 2
)
SELECT AllDaysAndHours.dayofweek, AllDaysAndHours.hourofday, CASE WHEN OpenAppDaysAndTimes.numEvents IS NOT NULL THEN numEvents ELSE 0 END AS numEvents
FROM AllDaysAndHours LEFT JOIN OpenAppDaysAndTimes ON AllDaysAndHours.dayofweek=OpenAppDaysAndTimes.dayofweek AND AllDaysAndHours.hourofday=OpenAppDaysAndTimes.hourofday;
""")

rows = cur.fetchall()
numEvents = []
for r in rows:
    numEvents.append(r[2])
x = np.arange(1, len(numEvents) + 1)
ax[2].bar(x, numEvents)
xlabels = ['', 'Mon 12AM', 'Mon 12PM', 'Tue 12AM', 'Tue 12PM', 'Wed 12AM', 'Wed 12PM', 'Thurs 12AM', 'Thurs 12PM',
           'Fri 12AM', 'Fri 12PM', 'Sat 12AM', 'Sat 12PM', 'Sun 12AM', 'Sun 12PM']
ax[2].set_xticks(x)
ax[2].xaxis.set_minor_locator(MultipleLocator(3))
ax[2].xaxis.set_major_locator(MultipleLocator(12))
ax[2].set_title('Day of Week + Time of Day for Open App Events')
ax[2].set(xlabel='Day + Time', ylabel='# of Open App Events')
ax[2].set_xticklabels(xlabels)
ax[2].grid()

plt.tight_layout()


def saveFile(folderName):
    fileName = '/Hour of Day and Day of Week Usage.pdf'
    plt.savefig(folderName + fileName)


# plt.show()
def saveFile2(folderName):
    fileName = '/Hour of Day and Day of Week Usage - Clock.pdf'
    # Fun Clock Graph of By Hour Breakdown
    N = 23
    bottom = 2
    # create theta for 24 hours
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    # make the histogram that bined on 24 hour
    radii, tick = np.histogram(hours, bins=23)
    # width of each bin on the plot
    width = (2 * np.pi) / N
    # make a polar plot
    plt.figure(figsize=(10, 6))
    ax = plt.subplot(111, polar=True)
    bars = ax.bar(theta, radii, width=width, bottom=bottom)
    # set the lable go clockwise and start from the top
    ax.set_theta_zero_location("N")
    # clockwise
    ax.set_theta_direction(-1)
    # set the label
    ticks = ['12:00AM', '3:00AM', '6:00AM', '9:00AM', '12:00PM', '3:00PM', '6:00PM', '9:00PM']
    ax.set_xticklabels(ticks)
    ax.set_title('Hour of Day for Open App Events')
    plt.savefig(folderName + fileName)
    plt.close(fig)


conn.close()
