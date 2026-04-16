"""
Banner Grabber Module
Extracts service versions and banners from open ports
"""

import socket
import ssl
import http.client
from typing import Dict, Optional, Tuple
from rich.console import Console

console = Console()

class BannerGrabber:
    """
    Grabs banners and service information from open ports
    """
    
    def __init__(self, timeout: int = 10):
        """
        Initialize banner grabber
        
        Args:
            timeout: Socket timeout in seconds
        """
        self.timeout = timeout
    
    def grab_banner(self, host: str, port: int) -> Optional[str]:
        """
        Attempt to grab banner from a service
        
        Args:
            host: Target host IP or hostname
            port: Target port number
            
        Returns:
            Banner string or None if unable to grab
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, int(port)))
            
            # Receive initial banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner if banner else None
            
        except socket.timeout:
            return None
        except ConnectionRefusedError:
            return None
        except Exception as e:
            console.print(f"[dim]Banner grab error on {host}:{port} - {str(e)}[/dim]")
            return None
    
    def grab_http_banner(self, host: str, port: int, use_ssl: bool = False) -> Dict:
        """
        Grab HTTP headers and banner information
        
        Args:
            host: Target host
            port: Target port
            use_ssl: Use HTTPS/SSL
            
        Returns:
            Dictionary with HTTP information
        """
        try:
            if use_ssl:
                conn = http.client.HTTPSConnection(host, port, timeout=self.timeout)
            else:
                conn = http.client.HTTPConnection(host, port, timeout=self.timeout)
            
            conn.request("HEAD", "/")
            response = conn.getresponse()
            
            headers = dict(response.getheaders())
            
            return {
                'status_code': response.status,
                'server': headers.get('server', 'unknown'),
                'x_powered_by': headers.get('x-powered-by', ''),
                'content_type': headers.get('content-type', ''),
                'headers': headers
            }
            
        except Exception as e:
            console.print(f"[dim]HTTP banner grab error on {host}:{port} - {str(e)}[/dim]")
            return {}
        finally:
            try:
                conn.close()
            except:
                pass
    
    def grab_ssh_banner(self, host: str, port: int = 22) -> Optional[str]:
        """
        Grab SSH banner information
        
        Args:
            host: Target host
            port: SSH port (default 22)
            
        Returns:
            SSH banner string
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, port))
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner if banner else None
            
        except Exception as e:
            console.print(f"[dim]SSH banner grab error on {host}:{port} - {str(e)}[/dim]")
            return None
    
    def grab_smtp_banner(self, host: str, port: int = 25) -> Optional[str]:
        """
        Grab SMTP banner information
        
        Args:
            host: Target host
            port: SMTP port (default 25)
            
        Returns:
            SMTP banner string
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, port))
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner if banner else None
            
        except Exception as e:
            console.print(f"[dim]SMTP banner grab error on {host}:{port} - {str(e)}[/dim]")
            return None
    
    def grab_ftp_banner(self, host: str, port: int = 21) -> Optional[str]:
        """
        Grab FTP banner information
        
        Args:
            host: Target host
            port: FTP port (default 21)
            
        Returns:
            FTP banner string
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, port))
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner if banner else None
            
        except Exception as e:
            console.print(f"[dim]FTP banner grab error on {host}:{port} - {str(e)}[/dim]")
            return None
    
    def grab_banner_intelligent(self, host: str, port: int, service: str = None) -> Dict:
        """
        Intelligently grab banner based on service type
        
        Args:
            host: Target host
            port: Target port
            service: Service name (ssh, http, https, smtp, ftp, etc.)
            
        Returns:
            Dictionary with banner information
        """
        result = {
            'host': host,
            'port': port,
            'service': service,
            'banner': None,
            'details': {}
        }
        
        # Try service-specific grabbers
        if service == 'ssh' or port == 22:
            result['banner'] = self.grab_ssh_banner(host, port)
        elif service == 'smtp' or port == 25:
            result['banner'] = self.grab_smtp_banner(host, port)
        elif service == 'ftp' or port == 21:
            result['banner'] = self.grab_ftp_banner(host, port)
        elif service in ['http', 'https'] or port in [80, 443, 8080, 8443]:
            use_ssl = service == 'https' or port in [443, 8443]
            result['details'] = self.grab_http_banner(host, port, use_ssl)
            result['banner'] = result['details'].get('server', '')
        else:
            # Generic banner grab
            result['banner'] = self.grab_banner(host, port)
        
        return result
