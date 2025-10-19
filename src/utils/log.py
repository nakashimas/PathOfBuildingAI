import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s]: %(message)s",
)

LOG_HANDLER = logging.getLogger()
