"""
測試 Job Variables 的腳本
此腳本可以模擬 Worker 環境來測試配置
"""
import os
from config import Config

def test_job_variables():
    """測試 Job Variables 設定"""
    print("=== 測試 Job Variables ===")
    
    # 設定測試環境變數
    test_vars = {
        'REDIS_HOST': 'test-redis-host',
        'REDIS_PORT': '6380',
        'REDIS_DB': '1',
        'DISK_PATH': 'C:/test/',
        'FILTER_RULE': '.rar',
        'SOURCE_SERVER': 'test-source',
        'TARGET_SERVER': 'test-target',
        'TARGET_FOLDER': 'C:/test_output/'
    }
    
    print("設定測試環境變數...")
    for key, value in test_vars.items():
        os.environ[key] = value
        print(f"  {key} = {value}")
    
    print("\n從配置檔案讀取...")
    Config.print_current_config()
    
    print("\n清除測試環境變數...")
    for key in test_vars.keys():
        if key in os.environ:
            del os.environ[key]
    
    print("\n使用預設值...")
    Config.print_current_config()

def show_current_env():
    """顯示當前相關的環境變數"""
    print("=== 當前環境變數 ===")
    prefect_vars = [
        'REDIS_HOST', 'REDIS_PORT', 'REDIS_DB',
        'DISK_PATH', 'FILTER_RULE', 
        'SOURCE_SERVER', 'TARGET_SERVER', 'TARGET_FOLDER'
    ]
    
    for var in prefect_vars:
        value = os.getenv(var, '(未設定)')
        print(f"{var} = {value}")
    print("==================")

if __name__ == "__main__":
    print("Job Variables 測試工具")
    print("1. 顯示當前環境變數")
    show_current_env()
    
    print("\n2. 測試 Job Variables")
    test_job_variables()