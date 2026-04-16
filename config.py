# Configuration settings for the Vulnerability Scanner

# Scan speed settings
SCAN_SPEED = 'normal'  # options: slow, normal, fast

# Timeout settings
SCAN_TIMEOUT = 60  # in seconds

# API endpoints
API_ENDPOINTS = {
    'service_a': 'https://api.example.com/service_a',
    'service_b': 'https://api.example.com/service_b'
}

# Database settings
DATABASE_SETTINGS = {
    'db_host': 'localhost',
    'db_port': 5432,
    'db_user': 'user',
    'db_password': 'password',
    'db_name': 'vuln_scanner_db'
}