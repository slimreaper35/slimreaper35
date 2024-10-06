import time
from pathlib import Path

from celery import Task, chain, group
from polars import DataFrame

from db import mongo_manager
from tasks import get_browser, get_device, get_os, parse_log

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR.joinpath("data")


def enqueue_new_task(line: str) -> Task:
    info_group = group(get_browser.s(), get_device.s(), get_os.s())
    ch = chain(parse_log.s(line), info_group)
    task = ch.delay()
    return task


def parse_browsers(input_file: Path) -> None:
    mongo_manager.reset_collection()

    limit = 200

    with open(input_file) as file:
        for _ in range(limit):
            line = file.readline()
            enqueue_new_task(line)

    time.sleep(20)

    frequencies = dict()
    unique_browsers = mongo_manager.get_unique_values("browser")
    for browser in unique_browsers:
        frequencies[browser] = mongo_manager.count_key_value("browser", browser)

    data = {"BROWSER": frequencies.keys(), "FREQUENCY": frequencies.values()}
    df = DataFrame(data)

    print(df.sort(by="FREQUENCY", descending=True))


if __name__ == "__main__":
    logs = DATA_DIR.joinpath("apache-logs.txt")
    parse_browsers(logs)
