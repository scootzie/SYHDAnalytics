import os

import psycopg2 as p
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters

import constants

register_matplotlib_converters()

conn = p.connect(host=os.getenv('POSTGRES_HOST', constants.database_url), dbname=os.getenv('POSTGRES_DB', constants.database_name), user=os.getenv('POSTGRES_USER', constants.database_user), password=os.getenv('POSTGRES_PASSWORD', constants.database_password))
cur = conn.cursor()

# 6 Graphs
fig, ax = plt.subplots(nrows=2, ncols=3, figsize = (18, 8))


# Graph 1 - Demographics Breakdown - Device (Last 30 Days)
cur.execute("""
WITH mau AS (
    SELECT DISTINCT "memberID"
    FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN "Member" ON "Event"."memberID"="Member"."id"
    WHERE "Event"."createdAt"::DATE >= now()::DATE - 29
)
SELECT device, COUNT(*)
FROM "Member" JOIN mau ON "Member".id=mau."memberID"
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
FROM "Member"
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
    SELECT DISTINCT "memberID"
    FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN "Member" ON "Event"."memberID"="Member"."id"
    WHERE "Event"."createdAt"::DATE >= now()::DATE - 29
)
SELECT os, COUNT(*)
FROM "Member" JOIN mau ON "Member".id=mau."memberID"
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
FROM "Member"
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
    SELECT DISTINCT "memberID"
    FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN "Member" ON "Event"."memberID"="Member"."id"
    WHERE "Event"."createdAt"::DATE >= now()::DATE - 29
)
SELECT version, COUNT(*)
FROM "Member" JOIN mau ON "Member".id=mau."memberID"
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
FROM "Member"
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
