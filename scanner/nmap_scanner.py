import nmap

class NmapScanner:
    def __init__(self, target, stealth=True, speed=3):
        self.target = target
        self.stealth = stealth
        self.speed = speed
        self.scanner = nmap.PortScanner()

    def scan_ports(self):
        options = {}  # store options for nmap
        if self.stealth:
            options['-T'] = str(self.speed)
        self.scanner.scan(self.target, arguments='-sS -p- -sV --min-rate 1000', options=' '.join(f'{k} {v}' for k, v in options.items()))
        return self.scanner[self.target]['tcp']

    def parse_results(self, results):
        parsed_results = {}  # result parsing
        for port in results:
            parsed_results[port] = {
                'state': results[port]['state'],
                'service': results[port]['name'],
                'version': results[port]['version'],
            }
        return parsed_results

if __name__ == '__main__':
    target_ip = '192.168.1.1'  # Replace with the target IP address
    scanner = NmapScanner(target_ip)
    port_results = scanner.scan_ports()
    parsed = scanner.parse_results(port_results)
    print(parsed)