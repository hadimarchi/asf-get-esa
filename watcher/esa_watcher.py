# esa_watcher
# Author: Hal DiMarchi
# Grabs high interest SLC products from ESA

import logging
import os
from utils import execute, files, options, sql
from sentinelsat.sentinel import SentinelAPI

try:
    from psycopg2 import IntegrityError
except Exception:
    from psycopg2cffi._impl.exceptions import IntegrityError

logging.basicConfig(level=logging.DEBUG,
                    format='%(pathname)s %(asctime)s %(levelname)s %(message)s')


def find_candidate_files():
    logging.info("Getting products at ESA")

    api = SentinelAPI(options.user, options.password)
    products = api.query(limit=options.num_back, producttype="SLC")

    return products


def get_requested_files():
    return False


def insert_files_in_db(files):
    for file in files:
        try:
            esa_sql.do_esa_data_sql(options.insert_sql, {"granule": file[0],
                                                         "url": file[1]},)
        except IntegrityError as e:
            print(str(e))
        else:
            print("{} inserted".format(file[0]))


def filter_for_unknown(granule):  # get_status in old
    return True
    query = esa_sql.do_pg_sql(options.find_granules_in_pg_sql, {'name': granule})
    if len(query) > 0:
        logging.info("Status: {} {}".format(granule, "AVAILABLE"))
        return False
    logging.info("Status: {} {}".format(granule, "UNKNOWN"))
    return True


def intersects_subs(footprint):
    try:
        matches = esa_sql.do_hyp3_sql(options.intersects_hyp3_subs_sql.format(options.users),
                                      {'location': footprint})
    except Exception as e:
        print(str(e))
        logging.info("Geometry error?")
        logging.info("No matches")
        return False

    num_matches = int(matches[0][0]) if matches and matches[0] else None

    if num_matches:
        logging.info('Num matches: {}'.format(num_matches))
        return True

    logging.info('No matches')
    return False


if __name__ == "__main__":
    logging.info("Spinning up")
    Files = files.Files(os.path.dirname(__file__), logging)
    config_options = options.Config_and_Options(Files.config)
    config = config_options.config
    options = config_options.options
    esa_sql = sql.Esa_Sql(options)
    wanted_files = []

    if not get_requested_files():
        candidate_products = find_candidate_files()
    for product in candidate_products:
        if filter_for_unknown(candidate_products[product]['identifier']):
            if intersects_subs(candidate_products[product]['footprint']):
                wanted_files.append((candidate_products[product]['identifier'],
                                    candidate_products[product]['link_icon']))

    insert_files_in_db(wanted_files)
    esa_sql.close_connections()
    logging.info("Done")
