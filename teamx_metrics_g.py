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

# Graph 1 - % of users who have created a connection (CUMULATIVE)
cur.execute("""
SELECT (SELECT COUNT(DISTINCT memberID)
        FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID
        WHERE name='Create Connection')
        AS "# of members w/ Connections", 
        COUNT(DISTINCT memberID)
        AS "# of total members"
FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID;
""")
rows = cur.fetchall()
top = rows[0][0]
total = rows[0][1]
percent = rows[0][0] / rows[0][1]
other = 1-percent
labels='HAS CREATED', 'HAS NOT CREATED'

print('# of Members who have Created Connection = ' + str(top))
print('# of Total Members = ' + str(total))

fig, ax = plt.subplots(nrows=2, ncols=1)
ax[0].pie([percent, other], labels=labels, autopct='%1.1f%%')
ax[0].set_title("% Breakdown (CUMULATIVE) of Members Who Create Connections")
ax[0].axis('equal')


# Graph 2 - % of new users (in the last 30 days) who have created at least one connection
cur.execute("""
WITH IDsOfNewMembersToCreateConnection AS (
    SELECT DISTINCT memberID AS id
    FROM Event JOIN MEMBER ON Event.memberID=Member.ID
    WHERE interactionID=4 AND Member.createdAt::DATE >= now()::DATE - 29
)
SELECT COUNT(*) AS numNewMembersToCreateAConnection, (SELECT COUNT(DISTINCT id)
        FROM MEMBER
        WHERE createdAt::DATE >= now()::DATE - 29) AS numNewMembers
FROM IDsOfNewMembersToCreateConnection
""")
rows1 = cur.fetchall()
top1 = rows1[0][0]
total1 = rows1[0][1]
percent1 = rows1[0][0] / rows1[0][1]
other1 = 1-percent1
labels1='NEW MEMBER HAS CREATED', 'NEW MEMBER HAS NOT CREATED'

print('# of New Members (Last 30 Days) who have Created Connection = ' + str(top1))
print('# of New Members (Last 30 Days) = ' + str(total1))

ax[1].pie([percent1, other1], labels=labels1, autopct='%1.1f%%')
ax[1].set_title("% of new users (in the last 30 days) who have created at least one connection")
ax[1].axis('equal')

plt.tight_layout()
plt.show()


conn.close()
