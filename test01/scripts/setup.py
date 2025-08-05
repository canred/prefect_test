"""Quick setup script for the Prefect project"""
import os
import subprocess
import sys


def setup_project():
    """Setup the Prefect project"""
    print("Setting up Prefect Redis File Processing project...")
    
    # Check if in correct directory
    if not os.path.exists('prefect.yaml'):
        print("Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Install requirements
    print("Installing Python packages...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✓ Packages installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install packages")
        return False
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("Creating .env file...")
        try:
            with open('.env.example', 'r') as source:
                content = source.read()
            with open('.env', 'w') as target:
                target.write(content)
            print("✓ .env file created from template")
        except Exception as e:
            print(f"✗ Failed to create .env file: {e}")
    
    # Test imports
    print("Testing module imports...")
    try:
        sys.path.append(os.getcwd())
        from tasks.redis_tasks import connect_redis
        from tasks.file_tasks import scan_files
        from utils.helpers import get_env_variables
        print("✓ All modules imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    print("\n" + "="*50)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Ensure Redis is running")
    print("3. Run: python scripts\\run_flow.py")
    print("4. Or deploy: python scripts\\deploy.py")
    print("="*50)
    
    return True


if __name__ == "__main__":
    setup_project()
