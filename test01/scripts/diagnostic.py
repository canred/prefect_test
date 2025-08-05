"""Diagnostic script to test components"""
import sys
import os

# Add current directory to path
sys.path.append('.')

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    try:
        print("- Testing utils.helpers...")
        from utils.helpers import get_env_variables
        print("  ✓ utils.helpers imported successfully")
        
        print("- Testing environment variables...")
        env_vars = get_env_variables()
        print(f"  ✓ Environment variables: {env_vars}")
        
        print("- Testing Redis connection...")
        import redis
        r = redis.Redis(host=env_vars['redis_host'], 
                       port=int(env_vars['redis_port']), 
                       db=int(env_vars['redis_db']), 
                       decode_responses=True)
        r.ping()
        print("  ✓ Redis connection successful")
        
        print("- Testing file scanning...")
        import os
        disk_path = env_vars['disk_path']
        filter_rule = env_vars['filter_rule']
        if os.path.exists(disk_path):
            print(f"  ✓ Disk path exists: {disk_path}")
        else:
            print(f"  ⚠ Disk path does not exist: {disk_path}")
            
        print("- Testing Prefect flow import...")
        from flows.my_flow_working import redis_file_processing_flow
        print("  ✓ Flow imported successfully")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()

def run_simple_test():
    """Run a simple version without Prefect decorators"""
    print("\nRunning simple test...")
    try:
        from utils.helpers import get_env_variables
        env_vars = get_env_variables()
        
        import redis
        r = redis.Redis(host=env_vars['redis_host'], 
                       port=int(env_vars['redis_port']), 
                       db=int(env_vars['redis_db']), 
                       decode_responses=True)
        
        # Test basic operations
        test_key = "test_connection"
        r.set(test_key, "test_value")
        result = r.get(test_key)
        r.delete(test_key)
        
        print(f"  ✓ Redis test successful: {result}")
        
    except Exception as e:
        print(f"  ✗ Simple test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Prefect Flow Diagnostic ===")
    test_imports()
    run_simple_test()
    print("=== Diagnostic Complete ===")
