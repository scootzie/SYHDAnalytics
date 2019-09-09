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

# 4 Graphs
fig, ax = plt.subplots(nrows=2, ncols=2, figsize = (16,8))


# Graph 1 - NOTIFICATIONS ENABLED - % Breakdown (Cumulative) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, action, METHOD, COUNT(*)
FROM "Event" JOIN "InteractionType" ON "Event.interactiontypeID"="InteractionType.ID" JOIN MEMBER ON "Event.memberID"="Member.id"
WHERE name='Contact Connection' AND notificationsEnabled=TRUE
GROUP BY source, METHOD, action
ORDER BY 1;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0] + ", " + r[1] + ", " + r[2])
    count.append(r[3])

ax[0, 0].pie(count, labels=labels, autopct='%1.1f%%')
ax[0, 0].set_title("% Breakdown of Contact Connection Source\n[Notifications ENABLED][Cumulative]")
ax[0, 0].axis('equal')


# Graph 2 - NOTIFICATIONS DISABLED - % Breakdown (Cumulative) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, action, METHOD, COUNT(*)
FROM "Event" JOIN "InteractionType" ON "Event.interactiontypeID"="InteractionType.ID" JOIN MEMBER ON "Event.memberID"="Member.id"
WHERE name='Contact Connection' AND notificationsEnabled=FALSE
GROUP BY source, METHOD, action
ORDER BY 1;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0] + ", " + r[1] + ", " + r[2])
    count.append(r[3])

ax[0, 1].pie(count, labels=labels, autopct='%1.1f%%')
ax[0, 1].set_title("% Breakdown of Contact Connection Source\n[Notifications DISABLED][Cumulative]")
ax[0, 1].axis('equal')


# Graph 3 - NOTIFICATIONS ENABLED - % Breakdown (Last 30 Days) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, action, METHOD, COUNT(*)
FROM "Event" JOIN "InteractionType" ON "Event.interactiontypeID"="InteractionType.ID" JOIN MEMBER ON "Event.memberID"="Member.id"
WHERE name='Contact Connection' AND notificationsEnabled=TRUE AND "Event.createdAt"::DATE>now()::DATE-29
GROUP BY source, METHOD, action
ORDER BY 1;
""")

rows1 = cur.fetchall()

labels1 = []
count1 = []
for r in rows1:
    labels1.append(r[0] + ", " + r[1] + ", " + r[2])
    count1.append(r[3])

ax[1, 0].pie(count1, labels=labels1, autopct='%1.1f%%')
ax[1, 0].set_title("% Breakdown of Contact Connection Source\n[Notifications Enabled][Last 30 Days]")
ax[1, 0].axis('equal')


# Graph 4 - NOTIFICATIONS DISABLED - % Breakdown (Last 30 Days) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, action, METHOD, COUNT(*)
FROM "Event" JOIN "InteractionType" ON "Event.interactiontypeID"="InteractionType.ID" JOIN MEMBER ON "Event.memberID"="Member.id"
WHERE name='Contact Connection' AND notificationsEnabled=FALSE AND "Event.createdAt"::DATE>now()::DATE-29
GROUP BY source, METHOD, action
ORDER BY 1;
""")

rows1 = cur.fetchall()

labels1 = []
count1 = []
for r in rows1:
    labels1.append(r[0] + ", " + r[1] + ", " + r[2])
    count1.append(r[3])

ax[1, 1].pie(count1, labels=labels1, autopct='%1.1f%%')
ax[1, 1].set_title("% Breakdown of Contact Connection Source\n[Notifications Disabled][Last 30 Days]")
ax[1, 1].axis('equal')

fig.subplots_adjust(wspace=.6)
fig.subplots_adjust(hspace=.6)
#plt.show()
def saveFile(folderName):
    fileName = '/Contact Connection Breakdown by Notifications Enabled:Disabled.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()