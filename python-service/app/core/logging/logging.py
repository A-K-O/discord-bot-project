import logging.config
import atexit
import logging.handlers
import pathlib
import json

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[4]
LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE_PATH = LOG_DIR / "backend.log.jsonl"


def setup_logging():
    config_file = pathlib.Path(__file__).parent / "config.json"

    with open(config_file) as file:
        config = json.load(file)

    if "handlers" in config and "file" in config["handlers"]:
        config["handlers"]["file"]["filename"] = str(LOG_FILE_PATH)

    logging.config.dictConfig(config)

    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
