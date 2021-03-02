import os
import functools
import requests
import shutil
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import cgi
from urllib.parse import urlparse
import downloads_list as dw
import db


sched = BlockingScheduler()

def build_file_path(alias: str):
    variant_1 = os.path.join(dw.DIR, alias + "_1")
    variant_2 =  os.path.join(dw.DIR, alias + "_2")
    
    if os.path.exists(variant_2):
        return variant_1

    if os.path.exists(variant_1):
        return variant_2

    return variant_1

def extract_file_extension(response):
    cd = response.headers.get("content-disposition")
    extension = None
    if cd:
        _, params = cgi.parse_header(cd)   
        extension = params.get("filename")
    
    if not extension:
        fname = urlparse(response.url).path.split("/")[-1]
        extension = fname.split(".")[-1]

    return extension


def download_and_save(url: str, filename: str):
    with requests.get(url, timeout=5, stream=True) as r:
        ext = extract_file_extension(r)
        if ext:
            filename += f".{ext}" 

        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    print("done:", url)
    
@sched.scheduled_job('interval', id='update_job', hours=5, next_run_time=datetime.now())
def update_job():
    os.makedirs(dw.DIR, exist_ok=True)
    
    for target in dw.list:
        alias = target["alias"]
        filepath = build_file_path(alias)
        try:
            download_and_save(target["url"], filepath)
        except Exception as e:
            print(e)
            continue
        db.update_dw_path(alias, filepath)

sched.start()
