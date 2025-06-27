import requests
import base64
import os
import re
import socket
from urllib.parse import urlparse, parse_qs, unquote
from collections import defaultdict

# The README file is our source of truth for all subscription links.
REPO_README_URL = "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/readme.md"

OUTPUT_DIR = "subscriptions"

def discover_subscription_urls():
    """
    Fetches the repository's README and parses it to discover all subscription file URLs.
    """
    print(f"[*] Discovering subscription links from: {REPO_README_URL}")
    urls = set()
    try:
        response = requests.get(REPO_README_URL, timeout=30)
        response.raise_for_status()
        
        # Regex to find all markdown links pointing to the raw .txt files within the repo
        # Example: (https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless.txt)
        regex = r"\(https://raw\.githubusercontent\.com/soroushmirzaei/telegram-configs-collector/main/.+?\.txt\)"
        
        found_links = re.findall(regex, response.text)
        
        # Clean up the found links (remove the parentheses)
        urls = {link.strip('()') for link in found_links}
        
        if not urls:
             print("    ❌ ERROR: No subscription links found in the README. The format might have changed.")
             return []

        print(f"    ✅ Discovered {len(urls)} unique subscription links.")
        return list(urls)
        
    except requests.exceptions.RequestException as e:
        print(f"    ❌ ERROR: Could not fetch the README file. Reason: {e}")
        return []

def fetch_and_decode_configs(subscription_urls):
    """Fetches and decodes all server configurations from a list of URLs."""
    unique_configs = set()
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    
    print("\n[*] Starting to fetch configs from all discovered links...")
    total_links = len(subscription_urls)
    for i, url in enumerate(subscription_urls):
        print(f"    -> Processing link {i+1}/{total_links}: {url}")
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            # Some files might be direct configs, others Base64 encoded. Try to decode.
            try:
                decoded_content = base64.b64decode(response.text).decode('utf-8')
            except (base64.binascii.Error, UnicodeDecodeError):
                # If decoding fails, assume it's plain text
                decoded_content = response.text

            configs_from_link = {line.strip() for line in decoded_content.strip().split('\n') if line.strip()}
            unique_configs.update(configs_from_link)
            print(f"    ✅ Fetched {len(configs_from_link)} configs.")
        except Exception as e:
            print(f"    ❌ ERROR processing {url}: {e}")
            
    return unique_configs

def get_ip_version(hostname):
    """Determines if a hostname resolves to IPv4 or IPv6."""
    try:
        socket.inet_pton(socket.AF_INET, hostname)
        return 'ipv4'
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, hostname)
            return 'ipv6'
        except socket.error:
            try:
                addr_info = socket.getaddrinfo(hostname, None)
                return 'ipv6' if addr_info[0][0] == socket.AF_INET6 else 'ipv4'
            except socket.gaierror:
                return 'unknown'

def parse_config(uri):
    """Parses a config URI to extract details."""
    try:
        parsed_uri = urlparse(uri)
        protocol = parsed_uri.scheme
        hostname = parsed_uri.hostname or ''
        
        query_params = parse_qs(parsed_uri.query)
        network = query_params.get('type', ['tcp'])[0]
        security = query_params.get('security', ['none'])[0]
        
        if 'reality' in query_params or security == 'reality':
             security = 'reality'

        country = 'unknown'
        fragment = unquote(parsed_uri.fragment)
        country_match = re.search(r'\b([A-Z]{2})\b', fragment)
        if country_match:
            country = country_match.group(1).upper()

        ip_version = get_ip_version(hostname)

        return {'uri': uri, 'protocol': protocol, 'country': country, 'network': network, 'security': security, 'ip_version': ip_version}
    except Exception:
        return None

def generate_split_subscriptions(configs):
    """Categorizes configs and generates split subscription files."""
    if not configs:
        print("\n[!] No configs to process. Halting file generation.")
        return

    print(f"\n[*] Total unique configs found: {len(configs)}")
    print("[*] Parsing and categorizing all configs...")
    
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
                if key in categorized and value: # Ensure value is not None or empty
                    categorized[key][value.lower()].append(config_uri) # Use lowercase for filenames

    print(f"[*] Successfully parsed {parsed_count} configs.")
    print("[*] Generating split subscription files...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for category, groups in categorized.items():
        category_path = os.path.join(OUTPUT_DIR, category)
        os.makedirs(category_path, exist_ok=True)
        for group_name, group_configs in groups.items():
            if group_name and group_configs:
                file_path = os.path.join(category_path, f"{group_name}.txt")
                write_b64_file(file_path, group_configs)
    
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
    subscription_urls = discover_subscription_urls()
    if subscription_urls:
        all_configs = fetch_and_decode_configs(subscription_urls)
        generate_split_subscriptions(all_configs)
        print("\n[*] ✅ All tasks completed successfully!")
    else:
        print("\n[!] Halting execution because no subscription URLs were found.")
