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

# Graph 1 - Histogram of All Member's # of Connections (CUMULATIVE)
cur.execute("""
WITH numConnectionsAdded AS (
        SELECT memberID, COUNT(name) AS "#added"
        FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
        WHERE name='Create Connection'
        GROUP BY memberID
        ),
    numConnectionsDeleted AS (
        SELECT memberID, COUNT(name) AS "#deleted", MEMBERID-COUNT(name) AS "test"
        FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
        WHERE name='Delete Connection'
        GROUP BY memberID
)
SELECT CASE WHEN "#deleted" IS NULL THEN "#added" ELSE "#added"-"#deleted" END AS "# of connections"
FROM numConnectionsAdded LEFT JOIN numConnectionsDeleted ON numConnectionsAdded.memberID=numConnectionsDeleted.memberID;
""")
rows = cur.fetchall()

nums = []
for r in rows:
    nums.append(r[0])
bins = np.max(nums)-1

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
    SELECT DISTINCT memberID
    FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
    WHERE name='Open App' AND Event.createdAt>now()::DATE-30
),
numConnectionsAdded AS (
    SELECT memberID, COUNT(name) AS "#added"
    FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
    WHERE name='Create Connection'
    GROUP BY memberID
),
numConnectionsDeleted AS (
    SELECT memberID, COUNT(name) AS "#deleted"
    FROM Event JOIN InteractionType ON Event.interactiontypeID=InteractionType.ID
    WHERE name='Delete Connection'
    GROUP BY memberID
)
SELECT CASE WHEN "#deleted" IS NULL THEN "#added" ELSE "#added"-"#deleted" END AS "# of connections"
FROM numConnectionsAdded LEFT JOIN numConnectionsDeleted ON numConnectionsAdded.memberID=numConnectionsDeleted.memberID JOIN mau ON numConnectionsAdded.memberID=mau.memberID;
""")
rows = cur.fetchall()

nums = []
for r in rows:
    nums.append(r[0])
bins = np.max(nums)-1
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
