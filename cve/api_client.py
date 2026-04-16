import requests
import os
import time
import json

class CVEAPIClient:
    def __init__(self):
        self.nvd_url = 'https://api.nvd.nist.gov/vuln/v2'
        self.exploit_db_url = 'https://www.exploit-db.com/api/v1'
        self.cache = {}
        self.cache_duration = 3600  # 1 hour

    def fetch_nvd_data(self, cve_id):
        cache_key = f'nvd_{cve_id}'
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data

        response = requests.get(f'{self.nvd_url}/cve/{cve_id}')
        if response.status_code == 200:
            self.cache[cache_key] = (response.json(), time.time())
            return response.json()
        else:
            raise Exception('Failed to fetch data from NVD')

    def fetch_exploit_db_data(self, cve_id):
        cache_key = f'exploit_db_{cve_id}'
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data

        response = requests.get(f'{self.exploit_db_url}/search/{cve_id}')
        if response.status_code == 200:
            self.cache[cache_key] = (response.json(), time.time())
            return response.json()
        else:
            raise Exception('Failed to fetch data from Exploit-DB')

    def clear_cache(self):
        self.cache.clear()