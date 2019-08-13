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
SELECT frequency
FROM UpdateConnectionTypeContext
WHERE frequency IS NOT NULL;
""")

rows = cur.fetchall()
freqs = []
for r in rows:
    freqs.append(r[0])

bins = np.arange(0, max(freqs)+1, 1)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (12,6))

ax.hist(freqs, bins=bins+1)
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.set_xticks(bins)
ax.set_title('Breakdown of Reminder Frequency Changes')
ax.set(xlabel='# of weeks changed to', ylabel='# of events')

#plt.show()
def saveFile(folderName):
    fileName = '/Most Common Reminder Frequencies Set.pdf'
    plt.savefig(folderName + fileName)
    plt.close()

conn.close()