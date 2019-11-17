import os

import numpy as np
import psycopg2 as p
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters

import constants

register_matplotlib_converters()

conn = p.connect(host=os.getenv('POSTGRES_HOST', constants.database_url), dbname=os.getenv('POSTGRES_DB', constants.database_name), user=os.getenv('POSTGRES_USER', constants.database_user), password=os.getenv('POSTGRES_PASSWORD', constants.database_password))
cur = conn.cursor()

# Graph 1 - Histogram of All Member's # of Connections (CUMULATIVE)
cur.execute("""
WITH numConnectionsAdded AS (
        SELECT "memberID", COUNT(name) AS "#added"
        FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
        WHERE name='Create Connection'
        GROUP BY "memberID"
        ),
    numConnectionsDeleted AS (
        SELECT "memberID", COUNT(name) AS "#deleted", "memberID"-COUNT(name) AS "test"
        FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
        WHERE name='Delete Connection'
        GROUP BY "memberID"
)
SELECT CASE WHEN "#deleted" IS NULL THEN "#added" ELSE "#added"-"#deleted" END AS "# of connections"
FROM numConnectionsAdded LEFT JOIN numConnectionsDeleted ON numConnectionsAdded."memberID"=numConnectionsDeleted."memberID";
""")
rows = cur.fetchall()

nums = []
for r in rows:
    nums.append(r[0])
try:
    bins = np.max(nums)-1
except ValueError:
    bins = 1
    
plt.figure(figsize=(10,6))
plt.subplot(211)

plt.hist(nums, bins)
plt.title("Breakdown of Members by # of Connections (CUMULATIVE/ALL MEMBERS)")
plt.xlabel("# of Connections per Member")
plt.ylabel("# of Members")
plt.grid(alpha=0.5)


# Graph 2 - Histogram of All Member's # of Connections (MAUs)
cur.execute("""
WITH mau AS (
    SELECT DISTINCT "memberID"
    FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
    WHERE name='Open App' AND "Event"."createdAt">now()::DATE-30
),
numConnectionsAdded AS (
    SELECT "memberID", COUNT(name) AS "#added"
    FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
    WHERE name='Create Connection'
    GROUP BY "memberID"
),
numConnectionsDeleted AS (
    SELECT "memberID", COUNT(name) AS "#deleted"
    FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
    WHERE name='Delete Connection'
    GROUP BY "memberID"
)
SELECT CASE WHEN "#deleted" IS NULL THEN "#added" ELSE "#added"-"#deleted" END AS "# of connections"
FROM numConnectionsAdded LEFT JOIN numConnectionsDeleted ON numConnectionsAdded."memberID"=numConnectionsDeleted."memberID" JOIN mau ON numConnectionsAdded."memberID"=mau."memberID";
""")
rows = cur.fetchall()

nums = []
for r in rows:
    nums.append(r[0])
try:
    bins = np.max(nums)-1
except ValueError:
    bins = 1
plt.subplot(212)

plt.hist(nums, bins)
plt.title("Breakdown of Members by # of Connections (MAUs)")
plt.xlabel("# of Connections per Member")
plt.ylabel("# of Members")
plt.grid(alpha=0.5)


plt.subplots_adjust(hspace=.6)
#plt.show()
def saveFile(folderName):
    fileName = '/Number of Connections Breakdown.pdf'
    plt.savefig(folderName + fileName)
    plt.close()

conn.close()
