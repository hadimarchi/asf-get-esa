# esa_master_downloader.py
# script for managing downloading of high priority products
# from ESA
# Author: Hal DiMarchi

"""
Usage:
    esa_master_downloader.py [-v]
    esa_master_downloader.py -h | --help

Options:
    -v              verbose output to terminal
    -h --help       Show this screen

Setup:
    Create directory config

    Create file config/esa_master_downloader.cfg
    Fill according to the following:
        [general]
        password = (ESA password)
        ESA_host = https://scihub.copernicus.eu/apihub
        run = 1 (1 for run, 0 for stop)
        running = 0 (0 for not running, 1 for running. script will generally manage this value)
        wait_period = (number of seconds)

        [esa_data]
        user = (db user)
        pass = (db password)
        db = (database name)
        host = (database host)

        [sql]
        [sql]
        get_granule = select granule, url from granules where downloaded = false LIMIT 100
        download = update granules set downloaded = (%%(true_false)s) where granule = (%%(granule)s)

        [multiprocessing]
        max_processes = (1 to number of usernames)

        [users]
        usernames: ["username1", "username2", "username3", ...] (ESA users)

    Create file config/esa_child_downloader.cfg
    Fill according to the following:
        [general]
        download_dir = ./download (or any other desired path to download products to)
        password = (ESA password)
        ESA_host = https://scihub.copernicus.eu/apihub

"""
from docopt import docopt
import os
from master_utils import master, add_sys_out_handler_to_log

if __name__ == '__main__':
    master_downloader_cli_arguments = docopt(__doc__)
    if master_downloader_cli_arguments.get('-v'):
        add_sys_out_handler_to_log()

    master = master.Master(os.path.dirname(__file__))
    master.idle()
