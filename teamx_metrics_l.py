import psycopg2 as p
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.ticker import MultipleLocator

conn = p.connect(host=('POSTGRES_HOST', 'teamx'), dbname=os.getenv('POSTGRES_DB', 'teamx'), user=os.getenv('POSTGRES_USER', 'postgres'), password=os.getenv('POSTGRES_PASSWORD', ''))
cur = conn.cursor()


# 6 Graphs
fig, ax = plt.subplots(nrows=2, ncols=3, figsize = (14, 7))

# Graph 1 - % Breakdown (Cumulative) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, METHOD, COUNT(*)
FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
WHERE name='Update Connection' AND action='mark as contacted'
GROUP BY source, METHOD
ORDER BY 1;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0] + " (" + r[1] + ")")
    count.append(r[2])

ax[0][0].pie(count, labels=labels, autopct='%1.1f%%')
ax[0][0].set_title("'Mark as Contacted' Breakdown (CUMULATIVE)")
ax[0][0].axis('equal')



# Graph 2 - % Breakdown (Last 30 Days) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, METHOD, COUNT(*)
FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
WHERE name='Update Connection' AND action='mark as contacted' AND createdAt::DATE>now()::DATE-29
GROUP BY source, METHOD
ORDER BY 1;
""")

rows1 = cur.fetchall()

labels1 = []
count1 = []
for r in rows1:
    labels1.append(r[0] + " (" + r[1] + ")")
    count1.append(r[2])

ax[1][0].pie(count1, labels=labels1, autopct='%1.1f%%')
ax[1][0].set_title("'Mark as Contacted' Breakdown (LAST 30 DAYS)")
ax[1][0].axis('equal')



# Graph 3 - % Breakdown (Cumulative) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, METHOD, COUNT(*)
FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
WHERE name='Contact Connection' AND action='send text message'
GROUP BY source, METHOD
ORDER BY 1;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0] + " (" + r[1] + ")")
    count.append(r[2])

ax[0][1].pie(count, labels=labels, autopct='%1.1f%%')
ax[0][1].set_title("'Send Text Message' Breakdown (CUMULATIVE)")
ax[0][1].axis('equal')



# Graph 4 - % Breakdown (Last 30 Days) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, METHOD, COUNT(*)
FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
WHERE name='Contact Connection' AND action='send text message' AND createdAt::DATE>now()::DATE-29
GROUP BY source, METHOD
ORDER BY 1;
""")

rows1 = cur.fetchall()

labels1 = []
count1 = []
for r in rows1:
    labels1.append(r[0] + " (" + r[1] + ")")
    count1.append(r[2])

ax[1][1].pie(count1, labels=labels1, autopct='%1.1f%%')
ax[1][1].set_title("'Send Text Message' Breakdown (LAST 30 DAYS)")
ax[1][1].axis('equal')



# Graph 5 - % Breakdown (Cumulative) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, METHOD, COUNT(*)
FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
WHERE name='View Connection' AND action='view connection details'
GROUP BY source, METHOD
ORDER BY 1;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0] + " (" + r[1] + ")")
    count.append(r[2])

ax[0][2].pie(count, labels=labels, autopct='%1.1f%%')
ax[0][2].set_title("'View Connection Details' Breakdown (CUMULATIVE)")
ax[0][2].axis('equal')



# Graph 6 - % Breakdown (Last 30 Days) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, METHOD, COUNT(*)
FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
WHERE name='View Connection' AND action='view connection details' AND createdAt::DATE>now()::DATE-29
GROUP BY source, METHOD
ORDER BY 1;
""")

rows1 = cur.fetchall()

labels1 = []
count1 = []
for r in rows1:
    labels1.append(r[0] + " (" + r[1] + ")")
    count1.append(r[2])

ax[1][2].pie(count1, labels=labels1, autopct='%1.1f%%')
ax[1][2].set_title("'View Connection Details' Breakdown (LAST 30 DAYS)")
ax[1][2].axis('equal')

fig.subplots_adjust(wspace=1.5)

#plt.show()
def saveFile(folderName):
    fileName = '/Mark as Contacted, Send Message, and View Connection Details Breakdown.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()
