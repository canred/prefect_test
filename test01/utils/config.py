"""
配置檔案 - 使用 Prefect Job Variables
此檔案定義了如何從環境變數取得配置參數
"""
import os
from typing import Dict, Any

class Config:
    """配置類別，使用環境變數來管理配置參數"""
    
    @staticmethod
    def get_redis_config() -> Dict[str, Any]:
        """取得 Redis 連線設定"""
        return {
            "host": os.getenv('REDIS_HOST', 'localhost'),
            "port": int(os.getenv('REDIS_PORT', '6379')),
            "db": int(os.getenv('REDIS_DB', '0')),
            "decode_responses": True
        }
    
    @staticmethod
    def get_disk_path() -> str:
        """取得磁碟路徑"""
        return os.getenv('DISK_PATH', 'E:/')
    
    @staticmethod
    def get_filter_rule() -> str:
        """取得篩選規則"""
        return os.getenv('FILTER_RULE', '.zip')
    
    @staticmethod
    def get_source_server() -> str:
        """取得來源伺服器"""
        return os.getenv('SOURCE_SERVER', 'pc10714')
    
    @staticmethod
    def get_target_server() -> str:
        """取得目標伺服器"""
        return os.getenv('TARGET_SERVER', 'pc10714new')
    
    @staticmethod
    def get_target_folder() -> str:
        """取得目標資料夾"""
        return os.getenv('TARGET_FOLDER', 'd:/new_folder')
    
    @staticmethod
    def print_current_config():
        """列印當前配置（用於除錯）"""
        print("=== 當前配置 ===")
        print(f"Redis Host: {Config.get_redis_config()['host']}")
        print(f"Redis Port: {Config.get_redis_config()['port']}")
        print(f"Redis DB: {Config.get_redis_config()['db']}")
        print(f"Disk Path: {Config.get_disk_path()}")
        print(f"Filter Rule: {Config.get_filter_rule()}")
        print(f"Source Server: {Config.get_source_server()}")
        print(f"Target Server: {Config.get_target_server()}")
        print(f"Target Folder: {Config.get_target_folder()}")
        print("================")

if __name__ == "__main__":
    # 測試配置
    Config.print_current_config()