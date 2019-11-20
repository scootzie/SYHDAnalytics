import os

import psycopg2 as p
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

    # Graph 1 - % of users who have created a connection (CUMULATIVE)
    cur.execute("""
    SELECT (SELECT COUNT(DISTINCT "memberID")
            FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
            WHERE name='Create Connection')
            AS "# of users w/ Connections", 
            COUNT(DISTINCT "memberID")
            AS "# of total users"
    FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id";
    """)
    rows = cur.fetchall()
    top = rows[0][0]
    total = rows[0][1]
    percent = rows[0][0] / rows[0][1]
    other = 1 - percent
    labels = 'HAS CREATED', 'HAS NOT CREATED'

    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12, 6))
    ax[0].pie([percent, other], labels=labels, autopct='%1.1f%%')
    ax[0].set_title("% Breakdown (CUMULATIVE) of Members Who Create Connections")
    ax[0].axis('equal')

    # Graph 2 - % of new users (in the last 30 days) who have created at least one connection
    cur.execute("""
    WITH IDsOfNewMembersToCreateConnection AS (
        SELECT DISTINCT "memberID" AS id
        FROM "Event" JOIN "Member" ON "Event"."memberID"="Member"."id" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id"
        WHERE name='Create Connection' AND "Member"."createdAt"::DATE >= now()::DATE - 29
    )
    SELECT COUNT(*) AS numNewMembersToCreateAConnection, (SELECT COUNT(DISTINCT id)
            FROM "Member"
            WHERE "createdAt"::DATE >= now()::DATE - 29) AS numNewMembers
    FROM IDsOfNewMembersToCreateConnection;
    """)
    rows1 = cur.fetchall()
    top1 = rows1[0][0]
    total1 = rows1[0][1]
    if rows1[0][1] > 0:
        percent1 = rows1[0][0] / rows1[0][1]
    else:
        percent1 = 0
    other1 = 1 - percent1
    labels1 = 'NEW "Member" HAS CREATED', 'NEW "Member" HAS NOT CREATED'

    ax[1].pie([percent1, other1], labels=labels1, autopct='%1.1f%%')
    ax[1].set_title("% of new users (in the last 30 days) who have created at least one connection")
    ax[1].axis('equal')

    plt.tight_layout()

    # plt.show()
    file_name = '/Members Who Create Connections.pdf'
    plt.savefig(folder + file_name)
    plt.close(fig)

    conn.close()
