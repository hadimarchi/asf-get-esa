# esa_watcher
# Author: Hal DiMarchi
# Grabs high interest SLC products from ESA

import logging
import os
from utils import execute, files, options, sql
try:
    import psycopg2
except Exception:
    import psycopg2cffi as psycopg2

logging.basicConfig(level=logging.DEBUG,
                    format='%(pathname)s %(asctime)s %(levelname)s %(message)s')


def find_candidate_files():
    logging.info("Getting products at ESA")
    file_list = []
    for i in range(options.num_back//options.inc):
        start = i*options.inc
        search_url = "https://" + config.get('general', 'ESA_host') + "/apihub/search?q=S1*&rows=" + str(options.inc) + "&start=" + str(start)
        Files.target_xml = Files.base_xml + '_' + str(start) + '_' + str(start+options.inc) + '.xml'
        cmd = 'wget -O ' + Files.target_xml + ' --user=' + options.user + ' --password=' + options.password + ' --no-check-certificate "' + search_url + '"'
        execute(cmd, logging, Files.target_xml, quiet=False)

        try:
            file_list.extend(Files.parse_esa_xml())
        except Exception as e:
            logging.error("Error:{} \n".format(str(e)))
            logging.error('Invalid XML!  ESA site is down?')

    return file_list


def get_requested_files():
    return False


def insert_files_in_db(files):
    for file in files:
        try:
            esa_sql.do_esa_data_sql(options.insert_sql, {"granule": file})
        except psycopg2._impl.exceptions.IntegrityError as e:
            print(str(e))


def filter_for_unknown(granule):  # get_status in old
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
        candidate_file_list = find_candidate_files()
    for file in candidate_file_list:
        if filter_for_unknown(file.get("title")):
            if intersects_subs(file.get("footprint")):
                wanted_files.append(file.get("title"))

    insert_files_in_db(wanted_files)
    esa_sql.close_connections()
    logging.info("Done")
