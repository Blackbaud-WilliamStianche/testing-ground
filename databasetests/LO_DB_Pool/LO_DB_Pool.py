#!/usr/bin/env python3

"""Python library for creating and using Luminate Online Database Connections within Python.

Requires:
    Third Party:
        cx_Oracle module (pip name is cx-Oracle): Used to handle connections and pools to individual
            Oracle database instances.
    Internal:
        lib/pythonlibs/luminate/utils.py: Used for gathering cluster and site specific data to
            to determine database connection details.


Classes:
    LO_DB_Pool: Parent Class used to create a connection pool to LO Database Servers within Python.
        It is best to not use this class directly, instead use Convio_Pool and/or Site_Pool.
    Convio_Pool: Class used for creating and handling a connection pool to the Convio Schema.
        Uses homogeneous pooling.
    Site_Pool: Classed used for creating and handling a connection pool to Site Schemas.
        Uses heterogeneous pooling so that each connection acquired can be used for a different site
        schema.

    Example text, delete below this line once docstring is complete.
    Cluster: Used for cluster wide data and operations.
             Examples:
                 is the cluster a production cluster cluster.is_prod
                 what is the list of DB's in the cluster cluster.db_list
    Site: Used for site specific data and operations.
          Examples:
              what DB is the site hosted on site.site_db
              where is the site's data directory site.site_data_dir
    SiteList: Used for creating iterable and interestingly indexed lists of Site objects.
              Examples:
                  create SiteList of sites with a subset of site_ids from a python list
                      utils.SiteList(key='cluster_id', sublist=somelist)
                  create SiteList of sites with the contents of a file containing short names
                      utils.SiteList(key='short', subfile='/some/path/to/file.txt')
"""

import cx_Oracle
from utils import Cluster


class LODBPool:
    def __init__(self, **kwargs):
        accepted_types = ('convio', 'site')

        if 'prod_file' in kwargs and 'db_file' in kwargs:
            self.cluster = Cluster(prod_file=kwargs['prod_file'], db_file=kwargs['db_file'])
        elif 'prod_file' in kwargs:
            self.cluster = Cluster(prod_file=kwargs['prod_file'])
        elif 'db_file' in kwargs:
            self.cluster = Cluster(db_file=kwargs['db_file'])
        else:
            self.cluster = Cluster()

        if 'type' not in kwargs or kwargs['type'] not in accepted_types:
            # TODO Add message about invalid or missing type parameter
            raise RuntimeError
        if 'db' not in kwargs or kwargs['db'] not in self.cluster.db_list:
            # TODO Add message about invalid or missing db parameter
            raise RuntimeError
        if kwargs['type'] != 'convio':
            if 'db_user' not in kwargs:
                # TODO Add messsage about missing db_user parameter
                raise RuntimeError
            if 'db_pass' not in kwargs:
                # TODO Add message about missing db_pass parameter
                raise RuntimeError

        if kwargs['type'] == 'convio':
            try:
                self.pool = cx_Oracle.SessionPool('convio', 'convio', kwargs['db'], min=2, max=5,
                                                  increment=1, encoding="UTF-8")
            except cx_Oracle.DatabaseError as error:
                print(error)






class Convio_Pool:
    pass


class Site_Pool:
    pass