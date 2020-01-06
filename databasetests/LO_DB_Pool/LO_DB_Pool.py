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
    """kwargs:
        prod_file: pathlike or filelike object to pass on to Cluster
        db_file: pathlike or filelike object to pass on to Cluster
        type: type of pool to create
            Options:
                convio: creates homogeneous pool to a single db with convio credentials
                site: creates heterogeneous pool to a single db where site credentials can be used
                    during connection acquisition.
                db: database sid/dsn to connect to
                min: minimum size of the pool
                max: maximum size of the pool"""

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
            raise ValueError("The 'type' kwarg is required and must contain a value "
                             "from {}".format(accepted_types))
        if 'db' not in kwargs or kwargs['db'] not in self.cluster.db_list:
            raise ValueError("The 'db' kwarg is required and must contain a value "
                             "from {}".format(self.cluster.db_list))
        if 'min' in kwargs:
            if kwargs['min'] < 1 or kwargs['min'] > 5:
                raise ValueError("The 'min' kwarg cannot exceed 5")
        else:
            kwargs['min'] = 1
        if 'max' in kwargs:
            if kwargs['max'] < 1 or kwargs['max'] > 10:
                raise ValueError("The 'max' kwarg cannot exceed 10")
        else:
            kwargs['max'] = 2

        if kwargs['type'] == 'convio':
            try:
                self.pool = cx_Oracle.SessionPool(user='convio', password='convio',
                                                  dsn=kwargs['db'], min=kwargs['min'],
                                                  max=kwargs['max'], increment=1, encoding="UTF-8")
            except cx_Oracle.DatabaseError as error:
                print(error)
                raise error
        elif kwargs['type'] == 'site':
            try:
                self.pool = cx_Oracle.SessionPool(dsn=kwargs['db'], min=kwargs['min'],
                                                  max=kwargs['max'], increment=1, encoding="UTF-8",
                                                  homogeneous=False)
            except cx_Oracle.DatabaseError as error:
                print(error)
                raise error


class ConvioPool(LODBPool):
    def __init__(self, **kwargs):
        super().__init__(type='convio', **kwargs)

    def get_connection(self):
        pass


class SitePool(LODBPool):
    def __init__(self, **kwargs):
        super().__init__(type='site', **kwargs)

    def get_connection(self, site):
        pass
