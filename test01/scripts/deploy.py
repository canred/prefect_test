"""Deployment script for Prefect Flow"""
import subprocess
import sys
import os


def deploy_flow():
    """Deploy the Prefect flow"""
    try:
        # Change to project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(project_dir)
        
        print("Deploying Prefect flow...")
        
        # Deploy the flow
        result = subprocess.run([
            'prefect', 'deploy', 'flows/my_flow.py:my_flow',
            '--name', 'redis-file-processing',
            '--work-pool', 'default_work'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Flow deployed successfully!")
            print(result.stdout)
        else:
            print("Deployment failed!")
            print(result.stderr)
            
    except Exception as e:
        print(f"Deployment error: {e}")


if __name__ == "__main__":
    deploy_flow()
