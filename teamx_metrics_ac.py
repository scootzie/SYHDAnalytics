import os

import numpy as np
import pandas as pd
import psycopg2 as p
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters

import constants


def plot_to_folder(folder):
    register_matplotlib_converters()

    conn = p.connect(host=os.getenv('POSTGRES_HOST', constants.database_url),
                     dbname=os.getenv('POSTGRES_DB', constants.database_name),
                     user=os.getenv('POSTGRES_USER', constants.database_user),
                     password=os.getenv('POSTGRES_PASSWORD', constants.database_password))
    cur = conn.cursor()

    cur.execute("""
    WITH CreateConnectionUsers AS(
        SELECT DISTINCT "Event"."memberID"
        FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
        WHERE name='Create Connection'
        ),
    dau AS (
        SELECT "createdAt"::DATE AS "date", count(DISTINCT "Event"."memberID") AS dau
        FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN CreateConnectionUsers ON "Event"."memberID"=CreateConnectionUsers."memberID"
        WHERE name='Open App'
        GROUP BY 1 
    )
    SELECT "date", dau, 
                (SELECT count(DISTINCT "Event"."memberID")
                FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN CreateConnectionUsers ON "Event"."memberID"=CreateConnectionUsers."memberID"
                WHERE name='Open App' AND "createdAt"::DATE BETWEEN dau.date - 7 AND dau.date) 
                AS wau,
                (SELECT count(DISTINCT "Event"."memberID")
                FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN CreateConnectionUsers ON "Event"."memberID"=CreateConnectionUsers."memberID"
                WHERE name='Open App' AND "createdAt"::DATE BETWEEN dau.date - 29 AND dau.date) 
                AS mau
    FROM dau;
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
        wauStick.append(r[2] - r[1])
        mauStick.append(r[3] - r[2])
    x = range(1, len(dates) + 1)

    # Graph 1 - DAU, WAU, and MAU Over Time
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 6))
    ax[0].plot(dates, dau, label='dau')
    ax[0].plot(dates, wau, label='wau')
    ax[0].plot(dates, mau, label='mau')
    ax[0].set_title("[USERS WHO HAVE CREATED 1+ CONNECTIONS] DAU, WAU, and MAU Over Time")
    ax[0].legend(loc='upper left')
    ax[0].set(xlabel='Date', ylabel='# of Active Users')
    # Make ticks on occurrences of each month:
    ax[0].xaxis.set_major_locator(mdates.MonthLocator())
    # Get only the month to show in the x-axis:
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax[0].grid(color='gray', linestyle='--')

    # Graph 2 - Stickiness (DAU/MAU and WAU/MAU)
    data = pd.DataFrame({'dau': dau, 'wau': wauStick, 'mau': mauStick, }, index=x)
    data_perc = data.divide(data.sum(axis=1), axis=0)
    ax[1].stackplot(dates, data_perc['dau'], data_perc['wau'], data_perc['mau'], labels=['dau', 'wau', 'mau'])
    ax[1].set_title("[USERS WHO HAVE CREATED 1+ CONNECTIONS] Stickiness - DAU and WAU over MAU")
    ax[1].legend(loc='upper left')
    ax[1].set(xlabel='Date', ylabel='DAU/MAU and WAU/MAU')
    # Make ticks on occurrences of each month:
    ax[1].xaxis.set_major_locator(mdates.MonthLocator())
    # Get only the month to show in the x-axis:
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax[1].set_yticks(np.arange(0.0, 1.1, 0.1))
    ax[1].grid(color='gray', linestyle='--')

    plt.tight_layout()

    # plt.show()
    file_name = '/1+ Connection Users - DAU, WAU, MAU, and Stickiness.pdf'
    plt.savefig(folder + file_name)
    plt.close(fig)

    conn.close()
