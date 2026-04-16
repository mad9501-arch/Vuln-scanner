import re
from typing import Dict, Tuple, Optional

class VersionDetector:
    VERSION_PATTERNS = {
        'apache': r'Apache(?:/| )([0-9.]+)',
        'nginx': r'nginx/([0-9.]+)',
        'openssh': r'OpenSSH[_\s]([0-9.]+)',
    }
    
    def extract_version(self, banner: str, service: str = None) -> Optional[Tuple[str, str]]:
        if not banner:
            return None
        
        if service and service in self.VERSION_PATTERNS:
            pattern = self.VERSION_PATTERNS[service]
            match = re.search(pattern, banner, re.IGNORECASE)
            if match:
                return (service, match.group(1))
        
        for service_name, pattern in self.VERSION_PATTERNS.items():
            match = re.search(pattern, banner, re.IGNORECASE)
            if match:
                return (service_name, match.group(1))
        
        return None