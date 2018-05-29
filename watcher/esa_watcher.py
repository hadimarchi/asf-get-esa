# esa_watcher
# Author: Hal DiMarchi
# Grabs high interest SLC products from ESA

"""
Usage:
    esa_watcher.py [-v]
    esa_watcher.py -h | --help

Options:
    -v              verbose output to terminal
    -h --help       Show this screen

Setup:
    Create directory config

    Create file config/esa_watcher.cfg
    Fill according to the following:
        [general]
        username = ESA username
        password = ESA Password
        users = [6, 14, 15, 16, 18, 25, 33, 31, 32]

        [hyp3-db]
        host = (hyp3db host)
        db = hyp3db
        user = (hyp3 username)
        pass = (hyp3 password)

        [pgsql]
        host = (pgsql db host)
        db = archive
        user =  (pgsqldb user)
        pass = (pgsqldb password)

        [esa_data]
        user = (esa_data_db user)
        pass = (esa_data_db password)
        db = esa_data_db
        host = (esa_data_db host)

        [fetch]
        num_back = 200 (number SLC examined, number GRD examined, half of total examined)
        group_size = 100 (number concurrently retrieved)
        [sql]
        pg_db_sql = select granule from sentinel where granule = %%(name)s
        intersects_subs_sql = select name from subscriptions where user_id in ({}) and enabled=True
                and ST_Intersects(location, ST_SetSRID(CAST(%%(location)s AS geometry), 4326))
        insert_sql = insert into granules (granule, url) values (%%(granule)s, %%(url)s)

"""

from docopt import docopt
import os
from utils import watcher, log, add_sys_out_handler_to_log


if __name__ == "__main__":
    log.info("Spinning up")
    watcher_cli_arguments = docopt(__doc__)
    if watcher_cli_arguments.get('-v'):
        add_sys_out_handler_to_log()

    watcher = watcher.Watcher(os.path.dirname(__file__))
    watcher.watch()
