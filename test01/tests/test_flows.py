"""Tests for Prefect Flow and Tasks"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tasks.redis_tasks import connect_redis, store_file_in_redis
from tasks.file_tasks import scan_files, create_file_data
from utils.helpers import get_env_variables


class TestRedisTasks(unittest.TestCase):
    """Test Redis related tasks"""
    
    @patch('redis.Redis')
    def test_connect_redis(self, mock_redis):
        """Test Redis connection"""
        mock_redis.return_value = MagicMock()
        
        with patch.dict(os.environ, {
            'REDIS_HOST': 'localhost',
            'REDIS_PORT': '6379',
            'REDIS_DB': '0'
        }):
            result = connect_redis.fn()
            self.assertIsNotNone(result)
    
    def test_store_file_in_redis(self):
        """Test storing file in Redis"""
        mock_redis = MagicMock()
        mock_redis.exists.return_value = False
        
        file_data = {
            'source_folder': 'E:/',
            'source_server': 'pc10714',
            'task_type': 'compression'
        }
        file_key = 'test_key'
        
        result = store_file_in_redis.fn(mock_redis, file_data, file_key)
        self.assertTrue(result)


class TestFileTasks(unittest.TestCase):
    """Test file processing tasks"""
    
    @patch('os.walk')
    def test_scan_files(self, mock_walk):
        """Test file scanning"""
        mock_walk.return_value = [
            ('E:/', [], ['file1.zip', 'file2.txt', 'file3.zip'])
        ]
        
        result = scan_files.fn('E:/', '.zip')
        self.assertEqual(len(result), 2)
        self.assertTrue(all(f.endswith('.zip') for f in result))
    
    def test_create_file_data(self):
        """Test file data creation"""
        file_path = 'E:/test.zip'
        result_data, result_key = create_file_data.fn(
            file_path, 'E:/', 'pc10714', 'pc10714new', 'd:/new_folder'
        )
        
        self.assertIn('source_folder', result_data)
        self.assertIn('zip_file_path', result_data)
        self.assertIn('job_watch_file', result_key)


if __name__ == '__main__':
    unittest.main()
