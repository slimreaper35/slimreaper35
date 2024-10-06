import logging

from rich.logging import RichHandler

LOG_FORMAT = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# handlers
file_handler = logging.FileHandler(filename="general.log", mode="w")
stream_handler = logging.StreamHandler()
rich_handler = RichHandler(
    show_time=False,
    show_level=False,
    show_path=False,
    markup=True,
)


def my_filter(record: logging.LogRecord) -> bool:
    if record.lineno % 2 == 0:
        return True

    return False


if __name__ == "__main__":
    log.addHandler(rich_handler)
    rich_handler.setFormatter(LOG_FORMAT)

    log.info("aaa")
    log.info("bbb")
    log.info("ccc")
