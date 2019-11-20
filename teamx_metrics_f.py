import os

import numpy as np
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
    WITH AllDates AS (
    SELECT generate_series(MIN("createdAt")::DATE, now()::DATE, INTERVAL '1 day') AS someday
    FROM "Member"
    )
    SELECT AllDates.someday::DATE AS "date", COUNT("createdAt")
    FROM AllDates LEFT JOIN "Member" ON AllDates.someday::DATE="Member"."createdAt"::DATE
    GROUP BY 1
    ORDER BY 1
    """)
    rows = cur.fetchall()

    dates = []
    counts = []
    for r in rows:
        dates.append(r[0])
        counts.append(r[1])

    cur.execute("""
    WITH newmembers AS(
        WITH AllDates AS (
            SELECT generate_series(MIN("createdAt")::DATE, now()::DATE, INTERVAL '1 day') AS someday
            FROM "Member"
        )
        SELECT AllDates.someday::DATE AS "date", COUNT("createdAt")
        FROM AllDates LEFT JOIN "Member" ON AllDates.someday::DATE="Member"."createdAt"::DATE
        GROUP BY 1
        ORDER BY 1
    )
    SELECT date, SUM(COUNT) OVER (ORDER BY DATE)::INT
    FROM newmembers;
    """)
    rows1 = cur.fetchall()

    dates1 = []
    counts1 = []
    for r in rows1:
        dates1.append(r[0])
        counts1.append(r[1])

    # Graph 1 - New Members Per Day
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 6))
    ax[0].plot(dates, counts)
    ax[0].set_title("# of New Members Per Day")
    ax[0].set(xlabel='Date (Month)', ylabel='# of New Members')
    # Make ticks on occurrences of each month:
    ax[0].xaxis.set_major_locator(mdates.MonthLocator())
    # Get only the month to show in the x-axis:
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax[0].yaxis.set_ticks(np.arange(0, max(counts) + 1, 1))
    ax[0].grid(color='gray', linestyle='--')

    # Graph 2 - New Members (Cumulative)
    ax[1].plot(dates1, counts1)
    ax[1].set_title("# of Total Members (Cumulative)")
    ax[1].set(xlabel='Date (Month)', ylabel='# of Members')
    # Make ticks on occurrences of each month:
    ax[1].xaxis.set_major_locator(mdates.MonthLocator())
    # Get only the month to show in the x-axis:
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax[1].yaxis.set_ticks(np.arange(0, max(counts1) + 1, 1))
    ax[1].grid(color='gray', linestyle='--')

    plt.tight_layout()

    # plt.show()
    file_name = '/New Members and Total Members.pdf'
    plt.savefig(folder + file_name)
    plt.close(fig)

    conn.close()
