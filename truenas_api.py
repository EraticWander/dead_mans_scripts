import requests
import json
import urllib3
from dotenv import load_dotenv
import os

class TrueNASAPI:
    """
    A class to interact with the TrueNAS API v2.0
    Handles authentication and basic CRUD operations
    """
    
    def __init__(self, verify_ssl=False):
        """
        Initialize the TrueNAS API client
        
        Args:
            verify_ssl (bool): Whether to verify SSL certificates (default: False)
        """
        load_dotenv()
        self.api_key = os.getenv("API_KEY")  # Load API key from .env file
        self.host = os.getenv("HOST")        # Load host from .env file
        self.verify_ssl = verify_ssl
        self.base_url = f"https://{self.host}/api/v2.0"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Disable SSL warning messages if verify_ssl is False
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
        self._verify_connection()
    
    def _request(self, method, endpoint, data=None):
        """
        Generic method to make HTTP requests to the TrueNAS API
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint path
            data (dict): Request payload data (optional)
            
        Returns:
            dict: JSON response from the API
            
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                verify=self.verify_ssl,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def get(self, endpoint):
        """
        Perform GET request to specified endpoint
        
        Args:
            endpoint (str): API endpoint path
            
        Returns:
            dict: JSON response from the API
        """
        return self._request('GET', endpoint)

    def post(self, endpoint, data):
        """
        Perform POST request to specified endpoint
        
        Args:
            endpoint (str): API endpoint path
            data (dict): Request payload data
            
        Returns:
            dict: JSON response from the API
        """
        return self._request('POST', endpoint, data)

    def put(self, endpoint, data):
        """
        Perform PUT request to specified endpoint
        
        Args:
            endpoint (str): API endpoint path
            data (dict): Request payload data
            
        Returns:
            dict: JSON response from the API
        """
        return self._request('PUT', endpoint, data)

    def delete(self, endpoint):
        """
        Perform DELETE request to specified endpoint
        
        Args:
            endpoint (str): API endpoint path
            
        Returns:
            dict: JSON response from the API
        """
        return self._request('DELETE', endpoint)
    
    def _verify_connection(self):
        """
        Verify connection to TrueNAS API by requesting system information
        
        Returns:
            dict: System information if successful, None if failed
        """
        try:
            response = self.get('system/info')
            print(f"Connection to {self.host} API successful!")
            return response
        except Exception as e:
            print(f"Failed to connect to {self.host} API: {str(e)}")
            return None

    def lock_dataset(self, dataset_id, force_umount=False):
        """
        Lock a ZFS dataset
        
        Args:
            dataset_id (str): ID/name of the dataset to lock
            force_umount (bool): Force unmount the dataset if mounted (default: False)
            
        Returns:
            dict: API response if successful, None if failed
        """
        data = {
                "id": f"{dataset_id}",
                "lock_options": {
                "force_umount": force_umount
                }
            }
        
        try:
            response = self.post("pool/dataset/lock", data)
            print(f"API Response: {json.dumps(response, indent=2)}")
            print(f"Dataset {dataset_id} locked successfully")
            return response
        except Exception as e:
            print(f"Failed to lock dataset {dataset_id}: {str(e)}")
            return None

if __name__ == "__main__":
    # Example usage
    api = TrueNASAPI()
    api.lock_dataset("Data/backup")
