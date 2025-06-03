import logging

from rich.logging import RichHandler

log = logging.getLogger(__name__)


def my_filter(record: logging.LogRecord) -> bool:
    if record.lineno % 2 == 0:
        return True

    return False


def setup_logging() -> None:
    _file_handler = logging.FileHandler(filename="general.log", mode="w")
    _stream_handler = logging.StreamHandler()
    _rich_handler = RichHandler(
        show_time=False,
        show_level=False,
        show_path=False,
        markup=True,
    )

    log_format = "%(asctime)s %(levelname)s %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[_rich_handler],
    )


setup_logging()

log.info("aaa")
log.warning("bbb")
log.error("ccc")
