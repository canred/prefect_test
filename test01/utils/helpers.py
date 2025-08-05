"""Helper functions for the Prefect Flow"""
from prefect import get_run_logger
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def log_job_variables():
    """Log all job variables for debugging"""
    logger = get_run_logger()
    
    logger.info("=== Job Variables Debug Information ===")
    logger.info(f"REDIS_HOST = {os.getenv('REDIS_HOST', 'localhost')}")
    logger.info(f"REDIS_PORT = {os.getenv('REDIS_PORT', '6379')}")
    logger.info(f"REDIS_DB = {os.getenv('REDIS_DB', '0')}")
    logger.info(f"DISK_PATH = {os.getenv('DISK_PATH', 'E:/')}")
    logger.info(f"FILTER_RULE = {os.getenv('FILTER_RULE', '.zip')}")
    logger.info(f"SOURCE_SERVER = {os.getenv('SOURCE_SERVER', 'pc10714')}")
    logger.info(f"TARGET_SERVER = {os.getenv('TARGET_SERVER', 'pc10714new')}")
    logger.info(f"TARGET_FOLDER = {os.getenv('TARGET_FOLDER', 'd:/new_folder')}")
    logger.info("================================")


def get_env_variables():
    """Get all environment variables as a dictionary"""
    return {
        'redis_host': os.getenv('REDIS_HOST', 'localhost'),
        'redis_port': os.getenv('REDIS_PORT', '6379'),
        'redis_db': os.getenv('REDIS_DB', '0'),
        'disk_path': os.getenv('DISK_PATH', 'E:/'),
        'filter_rule': os.getenv('FILTER_RULE', '.zip'),
        'source_server': os.getenv('SOURCE_SERVER', 'pc10714'),
        'target_server': os.getenv('TARGET_SERVER', 'pc10714new'),
        'target_folder': os.getenv('TARGET_FOLDER', 'd:/new_folder')
    }
