"""Working Redis File Processing Flow"""
from prefect import flow, task, get_run_logger
from dotenv import load_dotenv
import sys
import os
import redis
import datetime

# 設定編碼環境變數
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Load environment variables
load_dotenv()

@task
def scan_and_store_files():
    """Scan files and store them in Redis - single task approach"""
    logger = get_run_logger()
    
    try:
        
        # Get environment variables
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_db = int(os.getenv('REDIS_DB', '0'))
        disk_path = os.getenv('DISK_PATH', 'E:/')
        filter_rule = os.getenv('FILTER_RULE', '.zip')
        source_server = os.getenv('SOURCE_SERVER', 'pc10714')
        target_server = os.getenv('TARGET_SERVER', 'pc10714new')
        target_folder = os.getenv('TARGET_FOLDER', 'd:/new_folder')
        
        logger.info("=== Job Variables Debug Information ===")
        logger.info("Version:1.0.1")
        logger.info(f"REDIS_HOST = {redis_host}")
        logger.info(f"REDIS_PORT = {redis_port}")
        logger.info(f"REDIS_DB = {redis_db}")
        logger.info(f"DISK_PATH = {disk_path}")
        logger.info(f"FILTER_RULE = {filter_rule}")
        logger.info(f"SOURCE_SERVER = {source_server}")
        logger.info(f"TARGET_SERVER = {target_server}")
        logger.info(f"TARGET_FOLDER = {target_folder}")
        logger.info("================================")
        
        # Connect to Redis
        try:
            r = redis.Redis(
                host=redis_host, 
                port=redis_port, 
                db=redis_db, 
                decode_responses=True,
                socket_connect_timeout=5
            )
            r.ping()  # Test connection
            logger.info(f"Connected to Redis: {redis_host}:{redis_port}, DB: {redis_db}")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            return f"Redis connection failed: {e}"
        
        # Scan files on disk
        zip_files = []
        
        if os.path.exists(disk_path):
            for root, dirs, files in os.walk(disk_path):
                for file in files:
                    if file.endswith(filter_rule):
                        zip_files.append(os.path.join(root, file))
            logger.info(f"Found {len(zip_files)} {filter_rule} files in {disk_path}")
        else:
            logger.warning(f"Disk path does not exist: {disk_path}")
            logger.info("Continuing with empty file list for testing...")
        
        # Process each file
        stored_count = 0
        for file_path in zip_files:
            try:
                file_data = {
                    "source_folder": disk_path,
                    "source_server": source_server,
                    "task_type": "compression",
                    "to_server": target_server,
                    "to_folder": target_folder,
                    "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "init",
                    "try_count": 0,
                    "zip_file_path": file_path
                }
                
                # Generate Redis Key
                file_key = f"job_watch_file|{file_data['task_type']}|{file_data['source_server']}|{file_data['zip_file_path']}|{file_data['to_server']}|{file_data['to_folder']}"
                
                # Check if the same key already exists
                if r.exists(file_key):
                    logger.info(f"Key already exists, skipping: {file_key}")
                    continue
                
                # Store each key-value pair individually
                for key, value in file_data.items():
                    r.hset(file_key, key, value)
                
                logger.info(f"Stored file in Redis, Key: {file_key}")
                stored_count += 1
                
            except Exception as e:
                logger.error(f"Failed to process file {file_path}: {e}")
                continue
        
        result = f"Processed {len(zip_files)} files, stored {stored_count} new entries in Redis"
        logger.info(f"Task completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Task execution failed: {str(e)}")
        raise

@flow
def redis_file_processing_flow():
    """Main Redis File Processing Flow"""
    logger = get_run_logger()
    
    try:
        logger.info("Starting Redis File Processing Flow...")
        
        result = scan_and_store_files()
        
        logger.info(f"Flow execution completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Flow execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    print("Running Redis File Processing Flow...")
    try:
        result = redis_file_processing_flow()
        print(f"Success: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
