"""File processing tasks for Prefect Flow"""
from prefect import task, get_run_logger
import os
import datetime


@task
def scan_files(disk_path, filter_rule):
    """Scan files on disk based on filter rule"""
    logger = get_run_logger()
    
    try:
        zip_files = []
        
        for root, dirs, files in os.walk(disk_path):  # Recursively search disk
            for file in files:
                if file.endswith(filter_rule):  # Filter files with specified extension
                    zip_files.append(os.path.join(root, file))

        logger.info(f"Found {len(zip_files)} {filter_rule} files in {disk_path}")
        return zip_files
    except Exception as e:
        logger.error(f"Failed to scan files: {str(e)}")
        raise


@task
def create_file_data(file_path, disk_path, source_server, target_server, target_folder):
    """Create file data structure for Redis storage"""
    logger = get_run_logger()
    
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
        
        logger.info(f"Created file data for: {file_path}")
        return file_data, file_key
    except Exception as e:
        logger.error(f"Failed to create file data: {str(e)}")
        raise
