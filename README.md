### asf-get-esa

#### Installation:
1. RUN: pip3 install -r requirements.txt

#### Usage:
##### Downloader:
RUN: `python3 esa_master_downloader.py`

RUN: `python3 esa_master_downloader.py -h` for more setup information

This script checks the esa_data_db database once every given number of seconds.
If there are undownloaded products in the db the script will grab up to 100 of them
and download them with asynchronous multiprocessing. Otherwise the script will
resume waiting for new products.

##### Watcher:
RUN: `python3 esa_watcher.py`

RUN: `python3 esa_watcher.py -h` for more setup information


This script checks ESA sentinel database using the scihub api, and retrieves new SLC and GRD products
for subscriptions owned by high priority Hyp3 users, if those products are not already available to ASF.
