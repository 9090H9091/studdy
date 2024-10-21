import logging
import coloredlogs
import os
from datetime import datetime

def setup_logger():
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Set up file handler
    file_handler = logging.FileHandler(
        filename=f'logs/bot.log',
        encoding='utf-8',
        mode='a'
    )
    
    # Configure logging format
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_handler.setFormatter(logging.Formatter(logging_format))
    
    # Set up logger
    logger = logging.getLogger('discord_bot')
    logger.addHandler(file_handler)
    
    # Set up colored console logging
    coloredlogs.install(
        level='INFO',
        logger=logger,
        fmt=logging_format
    )
    
    return logger

def get_logger(name):
    return logging.getLogger(name)
