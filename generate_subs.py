import requests
import base64
import re

# This is the source README file we will parse to find the links.
REPO_README_URL = "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/readme.md"
OUTPUT_FILENAME = "All_Configs_Subscription.txt"

def discover_subscription_urls():
    """
    Fetches the repository's README and parses it to discover all subscription file URLs.
    This is a more robust method to ensure all links are found.
    """
    print(f"[*] Discovering subscription links from: {REPO_README_URL}")
    try:
        response = requests.get(REPO_README_URL, timeout=30)
        response.raise_for_status()
        
        # This regex finds all markdown-style links pointing to the collector's raw content.
        # It's designed to be flexible and capture all relevant URLs.
        regex = r"\(https://raw\.githubusercontent\.com/soroushmirzaei/telegram-configs-collector/main/[^)]+\)"
        found_links = re.findall(regex, response.text)
        
        # Clean up the found links (remove the parentheses) and remove duplicates.
        urls = sorted(list(set(link.strip('()') for link in found_links)))
        
        if not urls:
             print("    ❌ ERROR: No subscription links were found in the README. The format may have changed.")
             return []

        print(f"    ✅ Discovered {len(urls)} unique subscription links to process.")
        # Uncomment the following lines if you need to see all discovered URLs during a run.
        # for url in urls:
        #     print(f"        - {url}")
        return urls
        
    except requests.exceptions.RequestException as e:
        print(f"    ❌ ERROR: Could not fetch the README file. Reason: {e}")
        return []

def fetch_and_process_configs(subscription_urls):
    """
    Fetches configurations from all discovered URLs, decodes them, and returns a set of unique configs.
    """
    unique_configs = set()
    session = requests.Session()
    # Use a common user-agent to avoid being blocked.
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    
    print("\n[*] Starting to fetch configs from all discovered links...")
    total_links = len(subscription_urls)
    for i, url in enumerate(subscription_urls):
        # We print a shortened name for cleaner logs.
        print(f"    -> Processing link {i+1}/{total_links}: .../{'/'.join(url.split('/')[-2:])}")
        try:
            response = session.get(url, timeout=30)
            if response.status_code == 200:
                # Try to decode as Base64. If it fails, assume it's plain text.
                try:
                    content = base64.b64decode(response.text).decode('utf-8')
                except Exception:
                    content = response.text
                
                # Add each valid config line to our set to handle duplicates automatically.
                configs_from_link = {line.strip() for line in content.strip().split('\n') if line.strip()}
                unique_configs.update(configs_from_link)
                print(f"        ✅ Fetched {len(configs_from_link)} configs.")
            else:
                print(f"        ⚠️ WARNING: Skipped {url} (Status code: {response.status_code})")
        except Exception as e:
            print(f"        ❌ ERROR processing {url}: {e}")
            
    return unique_configs

def save_subscription_file(configs):
    """
    Saves the final set of unique configs into a single Base64-encoded file.
    """
    if not configs:
        print("\n[!] No configs were found. The output file will not be created.")
        return

    print(f"\n[*] Total unique configs found: {len(configs)}")
    
    # Sort the configs for a consistent output file.
    combined_str = "\n".join(sorted(list(configs)))
    
    # Encode the final combined string to Base64.
    encoded_str = base64.b64encode(combined_str.encode('utf-8')).decode('utf-8')
    
    try:
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(encoded_str)
        print(f"[*] ✅ Successfully created final subscription file: '{OUTPUT_FILENAME}'")
    except IOError as e:
        print(f"    ❌ ERROR: Could not write to file '{OUTPUT_FILENAME}'. Reason: {e}")

if __name__ == "__main__":
    # The main execution block
    discovered_urls = discover_subscription_urls()
    if discovered_urls:
        final_configs = fetch_and_process_configs(discovered_urls)
        save_subscription_file(final_configs)
    else:
        print("\n[!] Halting execution because no subscription URLs were found.")
