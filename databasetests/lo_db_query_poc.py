#!/usr/bin/env python3

import cx_Oracle
from utils import Cluster

CONVIO_SCHEMA_USER = "convio"
CONVIO_SCHEMA_PW = "convio"
CLUSTER = Cluster()
DB = CLUSTER.db_list[0]

try:
    with cx_Oracle.connect(CONVIO_SCHEMA_USER, CONVIO_SCHEMA_PW, DB, encoding="UTF-8") as connection:
        cursor = connection.cursor()
        for result in cursor.execute("select prefix, site_id from site_url"):
            print(result)
except cx_Oracle.DatabaseError as error:
    print(error)