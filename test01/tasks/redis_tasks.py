"""Redis related tasks for Prefect Flow"""
from prefect import task, get_run_logger
import redis
import os


@task
def connect_redis():
    """Connect to Redis using environment variables"""
    logger = get_run_logger()
    
    try:
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_db = int(os.getenv('REDIS_DB', '0'))
        
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
        
        logger.info(f"Connected to Redis: {redis_host}:{redis_port}, DB: {redis_db}")
        return r
    except Exception as e:
        logger.error(f"Redis connection failed: {str(e)}")
        raise


@task
def store_file_in_redis(redis_client, file_data, file_key):
    """Store file data in Redis"""
    logger = get_run_logger()
    
    try:
        # Check if the same key already exists
        if redis_client.exists(file_key):
            logger.info(f"Key already exists, skipping: {file_key}")
            return False
        
        # Store each key-value pair individually
        for key, value in file_data.items():
            redis_client.hset(file_key, key, value)
        
        logger.info(f"Stored file in Redis, Key: {file_key}")
        return True
    except Exception as e:
        logger.error(f"Failed to store file in Redis: {str(e)}")
        raise
