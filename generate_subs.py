import requests
import base64
import os
import re
import socket
from urllib.parse import urlparse, parse_qs, unquote
from collections import defaultdict

# A curated list of the primary subscription links from the source repository.
SUBSCRIPTION_URLS = [
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/export/all_configs_base64.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/export/all_reality_configs_base64.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/export/all_vless_configs_base64.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/export/all_vmess_configs_base64.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/export/all_trojan_configs_base64.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/export/all_ss_configs_base64.txt"
]

OUTPUT_DIR = "subscriptions"

def fetch_and_decode_configs():
    """Fetches and decodes all server configurations."""
    unique_configs = set()
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    print("[*] Starting to fetch configs...")
    for i, url in enumerate(SUBSCRIPTION_URLS):
        print(f"    -> Processing link {i+1}/{len(SUBSCRIPTION_URLS)}: {url}")
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            decoded_content = base64.b64decode(response.text).decode('utf-8')
            configs_from_link = {line.strip() for line in decoded_content.strip().split('\n') if line.strip()}
            unique_configs.update(configs_from_link)
            print(f"    ✅ Fetched {len(configs_from_link)} configs.")
        except Exception as e:
            print(f"    ❌ ERROR processing {url}: {e}")
    return unique_configs

def get_ip_version(hostname):
    """Determines if a hostname resolves to IPv4 or IPv6."""
    try:
        # Check if it's already an IP address
        socket.inet_pton(socket.AF_INET, hostname)
        return 'ipv4'
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, hostname)
            return 'ipv6'
        except socket.error:
            # If not an IP, try to resolve it
            try:
                addr_info = socket.getaddrinfo(hostname, None)
                # Return the family of the first address found
                return 'ipv6' if addr_info[0][0] == socket.AF_INET6 else 'ipv4'
            except socket.gaierror:
                return 'unknown' # Domain doesn't resolve

def parse_config(uri):
    """Parses a config URI to extract details."""
    try:
        parsed_uri = urlparse(uri)
        protocol = parsed_uri.scheme
        hostname = parsed_uri.hostname or ''
        
        query_params = parse_qs(parsed_uri.query)
        network = query_params.get('type', ['tcp'])[0]
        security = query_params.get('security', ['none'])[0]
        
        # Override security for reality
        if security == 'reality' or 'reality' in query_params:
             security = 'reality'

        country = 'unknown'
        fragment = unquote(parsed_uri.fragment)
        country_match = re.search(r'\b([A-Z]{2})\b', fragment)
        if country_match:
            country = country_match.group(1)

        ip_version = get_ip_version(hostname)

        return {
            'uri': uri,
            'protocol': protocol,
            'country': country,
            'network': network,
            'security': security,
            'ip_version': ip_version
        }
    except Exception:
        return None

def generate_split_subscriptions(configs):
    """Categorizes configs and generates split subscription files."""
    if not configs:
        print("\n[!] No configs to process.")
        return

    print(f"\n[*] Total unique configs found: {len(configs)}")
    print("[*] Parsing and categorizing all configs...")
    
    # Use defaultdict to easily append to lists
    categorized = {
        "protocol": defaultdict(list),
        "country": defaultdict(list),
        "network": defaultdict(list),
        "security": defaultdict(list),
        "ip_version": defaultdict(list),
    }

    parsed_count = 0
    for config_uri in configs:
        parsed = parse_config(config_uri)
        if parsed:
            parsed_count += 1
            for key, value in parsed.items():
                if key in categorized:
                    categorized[key][value].append(config_uri)

    print(f"[*] Successfully parsed {parsed_count} configs.")
    print("[*] Generating split subscription files...")

    # Create the main output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for category, groups in categorized.items():
        category_path = os.path.join(OUTPUT_DIR, category)
        os.makedirs(category_path, exist_ok=True)
        for group_name, group_configs in groups.items():
            if group_name and group_configs:
                file_path = os.path.join(category_path, f"{group_name}.txt")
                write_b64_file(file_path, group_configs)
    
    # Generate the single file with all configs
    write_b64_file(os.path.join(OUTPUT_DIR, "All_Configs.txt"), configs)
    print("\n[*] Main file 'All_Configs.txt' created.")

def write_b64_file(filepath, configs_list):
    """Writes a list of configs to a file after Base64 encoding."""
    print(f"    -> Writing {len(configs_list)} configs to {filepath}")
    combined_str = "\n".join(sorted(list(configs_list)))
    encoded_str = base64.b64encode(combined_str.encode('utf-8')).decode('utf-8')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(encoded_str)
    except IOError as e:
        print(f"    ❌ ERROR writing to {filepath}: {e}")

if __name__ == "__main__":
    all_configs = fetch_and_decode_configs()
    generate_split_subscriptions(all_configs)
    print("\n[*] ✅ All tasks completed successfully!")
