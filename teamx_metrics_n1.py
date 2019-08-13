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

# Set up Notifications Enabled Data
cur.execute("""
WITH notificationsEnabledDau AS (
  SELECT Event.createdAt::DATE AS "date", count(DISTINCT memberid) AS dau
  FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID JOIN MEMBER ON Event.memberID=Member.ID
  WHERE name='Open App' AND Member.notificationsEnabled=TRUE
  GROUP BY 1 
)
SELECT "date", dau, 
            (SELECT count(DISTINCT memberid)
            FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID JOIN MEMBER ON Event.memberID=Member.ID
            WHERE name='Open App' AND Member.notificationsEnabled=TRUE AND Event.createdAt::DATE BETWEEN notificationsEnabledDau.date - 7 AND notificationsEnabledDau.date) 
            AS wau,
            (SELECT count(DISTINCT memberid)
            FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID JOIN MEMBER ON Event.memberID=Member.ID
            WHERE name='Open App' AND Member.notificationsEnabled=TRUE AND Event.createdAt::DATE BETWEEN notificationsEnabledDau.date - 29 AND notificationsEnabledDau.date) 
            AS mau
FROM notificationsEnabledDau
""")

rows = cur.fetchall()
dates = []
dau = []
wau = []
mau = []
wauStick = []
mauStick = []
for r in rows:
    dates.append(r[0])
    dau.append(r[1])
    wau.append(r[2])
    mau.append(r[3])
    wauStick.append(r[2]-r[1])
    mauStick.append(r[3]-r[2])
x = range(1, len(dates)+1)


#Set Up Notifications Disabled Data
cur.execute("""
WITH notificationsDisabledDau AS (
  SELECT Event.createdAt::DATE AS "date", count(DISTINCT memberid) AS dau
  FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID JOIN MEMBER ON Event.memberID=Member.ID
  WHERE name='Open App' AND Member.notificationsEnabled=FALSE
  GROUP BY 1 
)
SELECT "date", dau, 
            (SELECT count(DISTINCT memberid)
            FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID JOIN MEMBER ON Event.memberID=Member.ID
            WHERE name='Open App' AND Member.notificationsEnabled=FALSE AND Event.createdAt::DATE BETWEEN notificationsDisabledDau.date - 7 AND notificationsDisabledDau.date) 
            AS wau,
            (SELECT count(DISTINCT memberid)
            FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID JOIN MEMBER ON Event.memberID=Member.ID
            WHERE name='Open App' AND Member.notificationsEnabled=FALSE AND Event.createdAt::DATE BETWEEN notificationsDisabledDau.date - 29 AND notificationsDisabledDau.date) 
            AS mau
FROM notificationsDisabledDau
""")

rows1 = cur.fetchall()
dates1 = []
dau1 = []
wau1 = []
mau1 = []
wauStick1 = []
mauStick1 = []
for r in rows1:
    dates1.append(r[0])
    dau1.append(r[1])
    wau1.append(r[2])
    mau1.append(r[3])
    wauStick1.append(r[2]-r[1])
    mauStick1.append(r[3]-r[2])
x1 = range(1, len(dates1)+1)

# 4 graphs
fig, ax = plt.subplots(nrows=2, ncols=2, figsize = (16,8))

# Graph 1 - ENABLED NOTIFICATIONS: DAU, WAU, and MAU Over Time
ax[0, 0].plot(dates, dau, label='dau')
ax[0, 0].plot(dates, wau, label='wau')
ax[0, 0].plot(dates, mau, label='mau')
ax[0, 0].set_title("ENABLED NOTIFICATIONS: DAU, WAU, and MAU Over Time")
ax[0, 0].legend(loc='upper left')
ax[0, 0].set(xlabel='Date', ylabel='# of Active Users')
# Make ticks on occurrences of each month:
ax[0, 0].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[0, 0].grid(color='gray', linestyle='--')

# Graph 2 - DISABLED NOTIFICATIONS: DAU, WAU, and MAU Over Time
ax[0, 1].plot(dates1, dau1, label='dau')
ax[0, 1].plot(dates1, wau1, label='wau')
ax[0, 1].plot(dates1, mau1, label='mau')
ax[0, 1].set_title("DISABLED NOTIFICATIONS: DAU, WAU, and MAU Over Time")
ax[0, 1].legend(loc='upper left')
ax[0, 1].set(xlabel='Date', ylabel='# of Active Users')
# Make ticks on occurrences of each month:
ax[0, 1].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[0, 1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[0, 1].grid(color='gray', linestyle='--')

# Graph 3 - ENABLED NOTIFICATIONS: Stickiness (DAU/MAU and WAU/MAU)
data = pd.DataFrame({'dau': dau, 'wau': wauStick, 'mau': mauStick, }, index=x)
data_perc = data.divide(data.sum(axis=1), axis=0)
ax[1, 0].stackplot(dates, data_perc['dau'], data_perc['wau'], data_perc['mau'], labels=['dau', 'wau', 'mau'])
ax[1, 0].set_title("ENABLED NOTIFICATIONS: Stickiness - DAU and WAU over MAU")
ax[1, 0].legend(loc='upper left')
ax[1, 0].set(xlabel='Date', ylabel='DAU/MAU and WAU/MAU')
# Make ticks on occurrences of each month:
ax[1, 0].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[1, 0].set_yticks(np.arange(0.0, 1.1, 0.1))
ax[1, 0].grid(color='gray', linestyle='--')

# Graph 4 - DISABLED NOTIFICATIONS: Stickiness (DAU/MAU and WAU/MAU)
data1 = pd.DataFrame({'dau': dau1, 'wau': wauStick1, 'mau': mauStick1, }, index=x1)
data_perc1 = data1.divide(data1.sum(axis=1), axis=0)
ax[1, 1].stackplot(dates1, data_perc1['dau'], data_perc1['wau'], data_perc1['mau'], labels=['dau', 'wau', 'mau'])
ax[1, 1].set_title("DISABLED NOTIFICATIONS: Stickiness - DAU and WAU over MAU")
ax[1, 1].legend(loc='upper left')
ax[1, 1].set(xlabel='Date', ylabel='DAU/MAU and WAU/MAU')
# Make ticks on occurrences of each month:
ax[1, 1].xaxis.set_major_locator(mdates.MonthLocator())
# Get only the month to show in the x-axis:
ax[1, 1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax[1, 1].set_yticks(np.arange(0.0, 1.1, 0.1))
ax[1, 1].grid(color='gray', linestyle='--')

fig.subplots_adjust(hspace=.6)
#plt.show()
def saveFile(folderName):
    fileName = '/DAU, WAU, MAU, Stickiness for Notifications Enabled:Disabled.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()