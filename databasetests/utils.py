"""Python library for various Luminate system management utility Classes.

Mimics much of the functionality of the bash cvset cvcalc functions but in python.

Classes:
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

import os
from pathlib import Path

# TODO Add LOGGER for logging to this module similar to what we have in robots_tool.py
# TODO Maybe add dev site indicator to Site class based on some criteria
# TODO add other relevant cluster specific things to this class. e.g. Web
#      Server list, SB Systems, LWS, FTP, etc.

CLUSTER_IDS = {'tc': 1, 'itc': 8, 2: 2, 3: 3}

class Cluster:
    """This class represents a Cluster and should contain various cluster specific items.

    Attributes:
        cluster_id: is the identifier for the cluster e.g. tc for test cluster, 2 for cluster 2
        cluster_number: is the numeric identifier for the cluster e.g. 1 for tc, 8 for itc, 2 for 2
        is_prod: is a boolean indicating if the cluster is a production cluster (Only 2 or 3)
        db_list: list containing SID's for the DB servers in the cluster e.g. ['db103tc, 'db104tc']
    """
    def __init__(self, prod_file='/etc/convio/conf/.production',
                 db_file='/etc/convio/conf/databases.csv'):
        self.cluster_id = None
        self.is_prod = None
        self.db_list = list()
        self.cluster_number = None

        # Read .production file and get cluster_id
        try:
            with open(prod_file, 'r') as input_file:
                self._process_prod_file_contents(input_file, prod_file)
        except IOError:
            raise RuntimeError("Unable to read from {}".format(prod_file))
        except TypeError:
            # Catches when ProdFile isn't PathLike and handles it like a File Object instead
            self._process_prod_file_contents(prod_file)

        # Validate cluster_id
        if self.cluster_id not in CLUSTER_IDS.keys():
            raise RuntimeError('Invalid cluster_id {} not in {}'.format(self.cluster_id,
                                                                        CLUSTER_IDS.keys()))
        # Initialize cluster_number
        self.cluster_number = CLUSTER_IDS[self.cluster_id]

        # Initialize is_prod
        if self.cluster_id == 2 or self.cluster_id == 3:
            self.is_prod = True
        else:
            self.is_prod = False

        # Populate db_list
        try:
            with open(db_file, 'r') as input_file:
                self._process_db_file_contents(input_file, db_file)
        except IOError:
            raise RuntimeError("Unable to read from {}".format(db_file))
        except TypeError:
            self._process_db_file_contents(db_file)

    def _process_prod_file_contents(self, input_file, file_name="unknown"):
        _lines = 0
        contents = input_file.readlines()
        for line in contents:
            _lines += 1
            try:
                self.cluster_id = int(line.rstrip())
            except ValueError:
                self.cluster_id = line.rstrip()

        if _lines > 1:
            raise RuntimeError('Improperly formatted .production file. '
                               'File {} contains more than a single line'.format(file_name))

    def _process_db_file_contents(self, input_file, file_name="unknown"):
        for line in input_file.readlines():
            try:
                db_value = line.split(',')[1]
            except IndexError:
                raise RuntimeError("Invalid databases.csv format in {}".format(file_name))
            if db_value[:3] == 'db' + str(self.cluster_number):
                self.db_list.append(db_value)
            else:
                raise RuntimeError("Invalid db_value {}"
                                   " in {} from file {}.".format(db_value, line, file_name))


# This class represents a Site based on similar structure to the site_version.csv and is intended
# to be initialized with data from that file.
# Yes, this could be implemented as a simple dictionary in its current form, however future plans
# include the ability to alter certain site specific values or fetch them from other sources on
# demand e.g. querying site_url for certain values but only when initially asked for then storing
# them in this object to prevent extra queries.
# TODO add functionality to populate various attributes based on definitive
#      sources (e.g. vhosts-jk for balgroup, etc.)
class Site:
    """This class represents a Site and should contain various site specific items.

    Attributes:
        site_id: numeric identifier for the site e.g. 3701
        short: string for the site's short name e.g. 'jdrf3'
        domain: string for the site's main domain (from site_version.csv for now)
        version: string for the version of Luminate Online that the site is on
        site_db: string for the DBSID that hosts the site
        site_data_root: string for the main site_data location in the cluster used for
            initializing site.site_data_dir
    """
    def __init__(self, site_id=None, short=None, domain=None, version=None, db=None,
                 site_data_dir='/etc/convio/site_data', balgrp=None):

        # We must have a value for site_id at the very least
        # TODO should probably add initialization checks here verify site_id and
        #      shortname match, verify site_id exists, pull missing data from site_version.csv
        # TODO add cluster designator as well should probably come with auto
        #      population from definitive source stuff.
        # TODO add db validator based on if the value is in db_list for the Cluster object
        self.site_id = site_id
        self.short = short
        self.domain = domain
        self.version = version
        self.site_db = db

        self.site_data_root = site_data_dir
        # Should add this back in but need a way to define it based on actual
        # configuration and not rely on site_version.csv since it can be incorrect.
        # self.balgrp = balgrp

    def __str__(self):
        # returns the Site as a string in JSON format for easy printing
        return '{ \"site_id\": ' + str(self.site_id) + ', \"short\": \"' + str(self.short) \
               + '\", \"domain\": \"' + str(self.domain) + '\", \"version\": \"' \
               + str(self.version) + '\", \"site_db\": \"' + str(self.site_db) + '\" }'

    def three(self):
        """Returns string of last three digits of the Site's site_id
        mimics functionality of cvcalc three 1234"""
        return str(self.site_id)[-3:]

    def eight(self):
        """Returns string of 8 digit representation left padded with 0's of the Site's site_id
        mimics functionality of cvcalc eight 1234"""
        return str(self.site_id).rjust(8, '0')

    def three_eight(self):
        """Returns string similar to 234/00001234 if site_id = 1234
        mimics functionality of cvcalc three-eight 1234"""
        return os.path.join(self.three(), self.eight())

    def site_data_dir(self):
        """Returns the full path for the root of a specific site's site_data directory
        e.g. /etc/convio/site_data/234/00001234 if the site_id were 1234"""
        return os.path.join(self.site_data_root, self.three_eight())


class SiteList:
    """This class represents an indexed iterable of Site objects.

    An interesting item of note is that SiteList items are indexable by both site_id and short.
    e.g. sitelist['3701'] should give you the Site with site_id 3701
    sitelist['jdrf3'] results in the Site with the matching short name.

    Attributes:
        shortkey: dictionary representation with short names as the keys
        idkey: dictionary representation with site ids as the keys
    """

    def __init__(self, **kwargs):
        """ kwargs description
            'all' - Boolean that determines if our SiteList will contain all sites in the cluster
                    when initialized or not
            'site_version' - String containing full path and filename to site_version.csv formatted
                             file containing all sites in the cluster
                             Note: defaults to /etc/convio/conf/site_version.csv when not defined
            'key' - String containing 'id' or 'short' determines what the source of a
                    sublist is providing for us to key off of when generating a SiteList that is a
                    subset of 'all' sites.
                    Note: When key='id' the items in sublist must be integers.
            'sublist' - A list containing items of 'key' for building our subset list
            'subfile' - String containing full path and filename to a text file containing a list of
                        'key' items to generate our subset of all sites
            'site_data_dir' - String containing full path to the main site_data location. Defaults
                              to '/etc/convio/site_data'. Should probably only be overriden when
                              testing in an environment where you have a copy of the site_data
                              structure and do not want to affect the real files.
        """

        self._list = list()  # is the List of Sites for doing iterable type things
        self.index = 0  # index for our _list iterable
        self.shortkey = {}  # dictionary representation with short names as the keys
        self.idkey = {}  # dictionary representation with site ids as the keys
        self._data_len = len(self._list)

        if 'site_version' not in kwargs:
            # TODO adjust logic here to allow StringIO of sample contents for site_version.csv
            # TODO should be something like if file kwargs['site_version'] doesn't exist then handle as StringIO
            kwargs['site_version'] = '/etc/convio/conf/site_version.csv'
        if 'site_data_dir' not in kwargs:
            kwargs['site_data_dir'] = '/etc/convio/site_data'
        if 'all' not in kwargs:
            kwargs['all'] = False
        if 'sublist' not in kwargs:
            kwargs['sublist'] = None
        if 'subfile' not in kwargs:
            kwargs['subfile'] = None

        if 'all' in kwargs and kwargs['all']:
            self._initialize_with_csv(filename=kwargs['site_version'],
                                      site_data_dir=kwargs['site_data_dir'])
        elif not kwargs['all'] and 'key' in kwargs and kwargs['key'] == 'short':
            self._initialize_with_csv_short_subset(filename=kwargs['site_version'],
                                                   site_data_dir=kwargs['site_data_dir'],
                                                   sublist=kwargs['sublist'],
                                                   subfile=kwargs['subfile'])
        else:
            if 'key' in kwargs and kwargs['key'] == 'id' and 'site_version' in kwargs:
                self._initialize_with_csv_id_subset(filename=kwargs['site_version'],
                                                    site_data_dir=kwargs['site_data_dir'],
                                                    sublist=kwargs['sublist'],
                                                    subfile=kwargs['subfile'])
            else:
                raise RuntimeError("ERROR: Unexpected initialization condition occurred.")

    def __len__(self):
        return self._data_len

    def __iter__(self):
        return self

    def __getitem__(self, item):
        return self._list[item]

    def __next__(self):
        self.index += 1
        try:
            return self._list[self.index-1]
        except IndexError:
            self.index = 0
            raise StopIteration

    def _initialize_with_csv(self, filename, site_data_dir):
        # filename must the the full path to a file that is in the format of site_version.csv
        # lines in filename starting with comment character '#' will be ignored

        try:
            with open(filename, 'r') as csvfile:
                contents = csvfile.readlines()
                for line in contents:
                    line = line.rstrip()
                    if line and line[0] != '#':
                        linelist = line.split(',')
                        siteid = int(linelist[0])
                        short = linelist[1]
                        domain = linelist[2]
                        version = linelist[3]
                        in_db = linelist[4]

                        site = Site(site_id=siteid, short=short, domain=domain,
                                    version=version, db=in_db, site_data_dir=site_data_dir)
                        self._list.append(site)
                        self.shortkey[short] = site
                        self.idkey[siteid] = site
        except IOError:
            raise RuntimeError("ERROR: Unable to read from {}".format(filename))

        self._data_len = len(self._list)

    def _initialize_with_csv_short_subset(self, filename, site_data_dir, sublist=None,
                                          subfile=None):
        # Filename must the the full path to a file that is in the format of site_version.csv
        # Must be called with either a sublist of short names OR a subfile containing short
        #     names never both
        # If used subfile needs to be the full path to a file containing short names one per line
        # Lines in filename starting with comment character '#' will be ignored

        if subfile and not sublist:
            sublist = list()
            try:
                with open(subfile, 'r') as list_file:
                    contents = list_file.readlines()
                    for line in contents:
                        line = line.rstrip()
                        if line and line[0] != '#':
                            sublist.append(line)
            except IOError:
                raise RuntimeError("ERROR: Unable to read from {}".format(filename))
        elif sublist and not subfile:
            if not sublist:
                raise RuntimeError("ERROR: _initialize_with_csv_short_subset called with invalid "
                                   "arguments\n"
                                   "filename={}\n"
                                   "sublist={}\n"
                                   "subfile={}\n"
                                   "The sublist must not be empty.".format(filename,
                                                                           sublist,
                                                                           subfile))
        else:
            raise RuntimeError("ERROR: _initialize_with_csv_short_subset called with invalid "
                               "arguments\n"
                               "filename={}\n"
                               "sublist={}\n"
                               "subfile={}\n"
                               "Only one parameter sublist or subfile can be "
                               "provided.".format(filename, sublist, subfile))

        try:
            with open(filename, 'r') as csvfile:
                for line in csvfile.readlines():
                    line = line.rstrip()
                    if line and line[0] != '#':
                        linelist = line.split(',')
                        siteid = int(linelist[0])
                        short = linelist[1]
                        if short in sublist:
                            site = Site(site_id=siteid, short=short, domain=linelist[2],
                                        version=linelist[3], db=linelist[4],
                                        site_data_dir=site_data_dir)
                            self._list.append(site)
                            self.shortkey[short] = site
                            self.idkey[siteid] = site
        except IOError:
            raise RuntimeError("ERROR: Unable to read from {}".format(filename))

        self._data_len = len(self._list)
        if self._data_len < 1:
            raise RuntimeError("ERROR: SiteList initialized with 0 sites.")

    def _initialize_with_csv_id_subset(self, filename, site_data_dir, sublist=None,
                                       subfile=None):
        # Filename must the the full path to a file that is in the format of site_version.csv
        # Must be called with either a sublist of site ids OR a subfile containing site ids
        #     never both
        # If used subfile needs to be the full path to a file containing site ids one per line
        # Lines in filename starting with comment character '#' will be ignored

        # print("filename={}\n"
        #       "sublist={}\n"
        #       "subfile={}".format(filename, sublist, subfile))

        if subfile and not sublist:
            sublist = list()
            try:
                with open(subfile, 'r') as listfile:
                    contents = listfile.readlines()
                    for line in contents:
                        line = line.rstrip()
                        if line and line[0] != '#':
                            line = int(line)
                            sublist.append(int(line))
            except IOError:
                raise RuntimeError("ERROR: Unable to read from {}".format(filename))
        elif sublist and not subfile:
            if not sublist:
                raise RuntimeError("ERROR: _initialize_with_csv_id_subset called with "
                                   "invalid arguments\n"
                                   "filename={}\n"
                                   "sublist={}\n"
                                   "subfile={}\n"
                                   "The sublist must not be empty.".format(filename,
                                                                           sublist, subfile))
        else:
            raise RuntimeError("ERROR: _initialize_with_csv_id_subset called with invalid "
                               "arguments\n"
                               "filename={}\n"
                               "sublist={}\n"
                               "subfile={}\n"
                               "Only one parameter sublist or subfile "
                               "can be provided.".format(filename, sublist, subfile))

        try:
            with open(filename, 'r') as csvfile:
                for line in csvfile.readlines():
                    line = line.rstrip()
                    if line and line[0] != '#':
                        linelist = line.split(',')
                        siteid = int(linelist[0])
                        short = linelist[1]
                        if siteid in sublist:
                            site = Site(site_id=siteid, short=short, domain=linelist[2],
                                        version=linelist[3], db=linelist[4],
                                        site_data_dir=site_data_dir)
                            self._list.append(site)
                            self.shortkey[short] = site
                            self.idkey[siteid] = site
        except IOError:
            raise RuntimeError("ERROR: Unable to read from {}".format(filename))

        self._data_len = len(self._list)
        if self._data_len < 1:
            raise RuntimeError("ERROR: SiteList initialized with 0 sites.")
