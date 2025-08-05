"""Script to run the Prefect flow locally"""
import sys
import os


# 設定編碼環境變數
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'


# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from flows.my_flow_working import redis_file_processing_flow

def run_flow():
    """Run the flow locally"""
    try:
        print("Starting Prefect flow execution...")
        result = redis_file_processing_flow()
        print(f"Flow completed successfully: {result}")
    except Exception as e:
        print(f"Flow execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_flow()
