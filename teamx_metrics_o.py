import os

import numpy as np
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

    # 2 Graphs
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12, 6))

    # Graph 1 - # of Unique Members who Create Connection --> Contact Connection (CUMULATIVE)
    cur.execute("""
    WITH createConnectionMembers AS (
        SELECT DISTINCT "Member"."id"
        FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN "Member" ON "Event"."memberID"="Member"."id"
        WHERE name='Create Connection'
    )
    SELECT COUNT(*) AS numMembersCreate, 
        (SELECT COUNT(DISTINCT createConnectionMembers.id) 
        FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN createConnectionMembers ON "Event"."memberID"=createConnectionMembers.id
        WHERE "InteractionType".name='Contact Connection') AS numMembersContact
    FROM createConnectionMembers;
    """)

    rows = cur.fetchall()
    data = [rows[0][0], rows[0][1], (rows[0][1] / rows[0][0])]
    labels = ['', 'Create Connection', 'Contact Connection', '% Conversion']
    x = np.arange(1, len(data) + 1)

    ax[0].bar(x + 1, data)
    ax[0].xaxis.set_major_locator(plt.MaxNLocator(3))
    for index, d in enumerate(data):
        if index == 2:
            ax[0].text(x=index + 2, y=d + 1, s="{round(d*100, 2)}%", fontdict=dict(fontsize=12))
        else:
            ax[0].text(x=index + 2, y=d - 1, s="{d}", fontdict=dict(fontsize=12))
    ax[0].set_xticklabels(labels)
    ax[0].set_ylabel('"Event" Type')
    ax[0].set_ylabel('# of Unique Members')
    ax[0].set_title('# of Unique Members who Create Connection --> Contact Connection (CUMULATIVE)')

    # Graph 2 - # of Unique Members who Create Connection --> Contact Connection (LAST 30 DAYS)
    cur.execute("""
    WITH createConnectionMembers AS (
        SELECT DISTINCT "Member"."id"
        FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN "Member" ON "Event"."memberID"="Member"."id"
        WHERE name='Create Connection' AND "Member"."createdAt"::DATE >= now()::DATE - 29
    )
    SELECT COUNT(*) AS numMembersCreate, 
        (SELECT COUNT(DISTINCT createConnectionMembers.id) 
        FROM "Event" JOIN "InteractionType" ON "Event"."interactionTypeID"="InteractionType"."id" JOIN createConnectionMembers ON "Event"."memberID"=createConnectionMembers.id
        WHERE "InteractionType".name='Contact Connection') AS numMembersContact
    FROM createConnectionMembers;
    """)

    rows = cur.fetchall()
    if rows[0][0] > 0:
        data = [rows[0][0], rows[0][1], (rows[0][1] / rows[0][0])]
    else:
        data = [rows[0][0], rows[0][1], 0]
    labels = ['', 'Create Connection', 'Contact Connection', '% Conversion']
    x = np.arange(1, len(data) + 1)

    ax[1].bar(x + 1, data)
    ax[1].xaxis.set_major_locator(plt.MaxNLocator(3))
    for index1, d1 in enumerate(data):
        if index1 == 2:
            ax[1].text(x=index1 + 2, y=d1 + 1, s="{round(d1*100, 2)}%", fontdict=dict(fontsize=12))
        else:
            ax[1].text(x=index1 + 2, y=d1 - 1, s="{d1}", fontdict=dict(fontsize=12))
    ax[1].set_xticklabels(labels)
    ax[1].set_ylabel('"Event" Type')
    ax[1].set_ylabel('# of Unique Members')
    ax[1].set_title('# of Unique Members who Create Connection --> Contact Connection (LAST 30 DAYS)')

    # plt.tight_layout()
    # plt.show()
    file_name = '/Members Who Create Connections and go on to Contact a Connection.pdf'
    plt.savefig(folder + file_name)
    plt.close(fig)

    conn.close()
