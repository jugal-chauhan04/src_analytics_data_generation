import logging
import os

def setup_logging(log_file = 'log/pipeline.log'):
    """
    Configure logging to include timestamps, duration, and messages
    """

    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler("pipeline.log"),
            logging.StreamHandler()
        ]
    )

    logging.info("Logging Initialized")