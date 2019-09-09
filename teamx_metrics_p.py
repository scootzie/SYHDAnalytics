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

# 6 Graphs
fig, ax = plt.subplots(nrows=2, ncols=3, figsize = (18, 8))


# Graph 1 - Demographics Breakdown - Device (Last 30 Days)
cur.execute("""
WITH mau AS (
    SELECT DISTINCT memberID
    FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID JOIN MEMBER ON Event.memberID=Member.ID
    WHERE Event.createdAt::DATE >= now()::DATE - 29
)
SELECT device, COUNT(*)
FROM MEMBER JOIN mau ON member.id=mau.memberid
GROUP BY device
ORDER BY device DESC;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0])
    count.append(r[1])

ax[0, 0].pie(count, labels=labels, autopct='%1.1f%%')
ax[0, 0].set_title("Demographics Breakdown - Device (Last 30 Days)")
ax[0, 0].axis('equal')


# Graph 2 - Demographics Breakdown - Device (All Members)
cur.execute("""
SELECT device, COUNT(*)
FROM MEMBER
GROUP BY device
ORDER BY device DESC;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0])
    count.append(r[1])

ax[1, 0].pie(count, labels=labels, autopct='%1.1f%%')
ax[1, 0].set_title("Demographics Breakdown - Device (All Members)")
ax[1, 0].axis('equal')


# Graph 3 - Demographics Breakdown - OS (Last 30 Days)
cur.execute("""
WITH mau AS (
    SELECT DISTINCT memberID
    FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID JOIN MEMBER ON Event.memberID=Member.ID
    WHERE Event.createdAt::DATE >= now()::DATE - 29
)
SELECT os, COUNT(*)
FROM MEMBER JOIN mau ON member.id=mau.memberid
GROUP BY os
ORDER BY os DESC;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0])
    count.append(r[1])

ax[0, 1].pie(count, labels=labels, autopct='%1.1f%%')
ax[0, 1].set_title("Demographics Breakdown - OS (Last 30 Days)")
ax[0, 1].axis('equal')


# Graph 4 - Demographics Breakdown - OS (All Members)
cur.execute("""
SELECT os, COUNT(*)
FROM MEMBER
GROUP BY os
ORDER BY os DESC;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0])
    count.append(r[1])

ax[1, 1].pie(count, labels=labels, autopct='%1.1f%%')
ax[1, 1].set_title("Demographics Breakdown - OS (All Members)")
ax[1, 1].axis('equal')


# Graph 5 - Demographics Breakdown - Version (Last 30 Days)
cur.execute("""
WITH mau AS (
    SELECT DISTINCT memberID
    FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID JOIN MEMBER ON Event.memberID=Member.ID
    WHERE Event.createdAt::DATE >= now()::DATE - 29
)
SELECT version, COUNT(*)
FROM MEMBER JOIN mau ON member.id=mau.memberid
GROUP BY version
ORDER BY version DESC;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0])
    count.append(r[1])

ax[0, 2].pie(count, labels=labels, autopct='%1.1f%%')
ax[0, 2].set_title("Demographics Breakdown - Version (Last 30 Days)")
ax[0, 2].axis('equal')


# Graph 6 - Demographics Breakdown - Version (All Members)
cur.execute("""
SELECT version, COUNT(*)
FROM MEMBER
GROUP BY version
ORDER BY version DESC;
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0])
    count.append(r[1])

ax[1, 2].pie(count, labels=labels, autopct='%1.1f%%')
ax[1, 2].set_title("Demographics Breakdown - Version (All Members)")
ax[1, 2].axis('equal')


#plt.show()
def saveFile(folderName):
    fileName = '/Demographics Breakdown.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()