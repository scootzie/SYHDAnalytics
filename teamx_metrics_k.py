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


# Graph 1 - % Breakdown (Cumulative) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, action, METHOD, COUNT(*)
FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID
WHERE name='Contact Connection'
GROUP BY source, METHOD, action
ORDER BY 1
""")

rows = cur.fetchall()
labels = []
count = []
for r in rows:
    labels.append(r[0] + ", " + r[1] + ", " + r[2])
    count.append(r[3])

fig, ax = plt.subplots(nrows=2, ncols=1, figsize = (12, 6))
ax[0].pie(count, labels=labels, autopct='%1.1f%%')
ax[0].set_title("% Breakdown (CUMULATIVE) of Contact Connection Source")
ax[0].axis('equal')



# Graph 2 - % Breakdown (Last 30 Days) of contact connection source/method/action - Pie Chart
cur.execute("""
SELECT source, action, METHOD, COUNT(*)
FROM Event JOIN Interaction ON Event.interactionID=Interaction.ID JOIN InteractionType ON Interaction.interactiontypeID=InteractionType.ID
WHERE name='Contact Connection' AND createdAt::DATE>now()::DATE-29
GROUP BY source, METHOD, action
ORDER BY 1
""")

rows1 = cur.fetchall()

labels1 = []
count1 = []
for r in rows1:
    labels1.append(r[0] + ", " + r[1] + ", " + r[2])
    count1.append(r[3])

ax[1].pie(count1, labels=labels1, autopct='%1.1f%%')
ax[1].set_title("% Breakdown (LAST 30 DAYS) of Contact Connection Source")
ax[1].axis('equal')


#plt.show()
def saveFile(folderName):
    fileName = '/Contact Connection Breakdown.pdf'
    plt.savefig(folderName + fileName)
    plt.close(fig)

conn.close()
