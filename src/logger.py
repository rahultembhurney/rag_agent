import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
import os

src_path = Path(__file__).resolve().parent
LOG_DIR = "logs"
log_file_name = f"{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.log"

log_dir_path = os.path.join(src_path, LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)
log_file_path = os.path.join(log_dir_path, log_file_name)

def configure_logger():

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s-%(name)s-%(levelname)s-%(message)s]")
    
    file_handler = RotatingFileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


configure_logger()

    
    
