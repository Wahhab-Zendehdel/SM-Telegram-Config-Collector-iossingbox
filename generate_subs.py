import os
import re
import requests
import json
from urllib.parse import urlparse, parse_qs, unquote
import base64
import binascii

# --- COUNTRY MAPPING ---
# Dictionary to map country codes to full names for the README
COUNTRY_CODES = {
    'al': 'Albania', 'ar': 'Argentina', 'am': 'Armenia', 'au': 'Australia',
    'at': 'Austria', 'bh': 'Bahrain', 'be': 'Belgium', 'bo': 'Bolivia',
    'ba': 'Bosnia & Herz.', 'br': 'Brazil', 'bg': 'Bulgaria', 'ca': 'Canada',
    'cl': 'Chile', 'cn': 'China', 'co': 'Colombia', 'cr': 'Costa Rica',
    'hr': 'Croatia', 'cy': 'Cyprus', 'cz': 'Czechia', 'dk': 'Denmark',
    'ec': 'Ecuador', 'ee': 'Estonia', 'fi': 'Finland', 'fr': 'France',
    'de': 'Germany', 'gi': 'Gibraltar', 'gr': 'Greece', 'gt': 'Guatemala',
    'hk': 'Hong Kong', 'is': 'Iceland', 'in': 'India', 'id': 'Indonesia',
    'ir': 'Iran', 'ie': 'Ireland', 'il': 'Israel', 'it': 'Italy', 'jp': 'Japan',
    'jo': 'Jordan', 'kz': 'Kazakhstan', 'kr': 'Korea', 'lv': 'Latvia',
    'lt': 'Lithuania', 'lu': 'Luxembourg', 'my': 'Malaysia', 'mt': 'Malta',
    'mu': 'Mauritius', 'mx': 'Mexico', 'md': 'Moldova', 'ma': 'Morocco',
    'mm': 'Myanmar', 'nl': 'Netherlands', 'nz': 'New Zealand', 'ng': 'Nigeria',
    'mk': 'North Macedonia', 'no': 'Norway', 'na': 'Not Available',
    'om': 'Oman', 'pk': 'Pakistan', 'py': 'Paraguay', 'pe': 'Peru',
    'ph': 'Philippines', 'pl': 'Poland', 'pt': 'Portugal', 'pr': 'Puerto Rico',
    'ro': 'Romania', 'ru': 'Russia', 'sa': 'Saudi Arabia', 'rs': 'Serbia',
    'sc': 'Seychelles', 'sg': 'Singapore', 'sk': 'Slovakia', 'si': 'Slovenia',
    'za': 'South Africa', 'es': 'Spain', 'se': 'Sweden', 'ch': 'Switzerland',
    'tw': 'Taiwan', 'th': 'Thailand', 'tr': 'Türkiye', 'ua': 'Ukraine',
    'ae': 'UAE', 'gb': 'UK', 'us': 'United States', 'vn': 'Viet Nam',
    'vg': 'Virgin Islands'
}


# --- CONFIG PARSING FUNCTIONS (No changes needed here) ---

def parse_vless(uri: str) -> dict | None:
    """Parses a VLESS URI and converts it to a sing-box outbound dictionary."""
    try:
        parsed_url = urlparse(uri)
        if not all([parsed_url.scheme == 'vless', parsed_url.username, parsed_url.hostname, parsed_url.port]):
            return None
        query_params = parse_qs(parsed_url.query)
        tag = unquote(parsed_url.fragment) if parsed_url.fragment else f"vless-{parsed_url.hostname}"
        config = {
            "type": "vless", "tag": tag, "server": parsed_url.hostname,
            "server_port": parsed_url.port, "uuid": parsed_url.username,
            "packet_encoding": "xudp",
        }
        transport_type = query_params.get('type', [None])[0]
        if transport_type:
            transport_config = {"type": transport_type}
            if transport_type == 'grpc':
                transport_config["service_name"] = query_params.get('serviceName', [''])[0]
            elif transport_type == 'ws':
                transport_config["path"] = unquote(query_params.get('path', ['/'])[0])
                if host := query_params.get('host', [None])[0]:
                    transport_config["headers"] = {"Host": host}
            config["transport"] = transport_config
        security = query_params.get('security', [None])[0]
        if security in ['tls', 'reality']:
            tls_config = {
                "enabled": True, "server_name": query_params.get('sni', [parsed_url.hostname])[0],
                "utls": {"enabled": True, "fingerprint": query_params.get('fp', ['chrome'])[0]}
            }
            if security == 'reality':
                if not (public_key := query_params.get('pbk', [None])[0]): return None
                reality_config = {"enabled": True, "public_key": public_key}
                if short_id := query_params.get('sid', [None])[0]:
                    reality_config["short_id"] = short_id
                tls_config['reality'] = reality_config
            config["tls"] = tls_config
        return config
    except Exception as e:
        print(f"Skipping VLESS URI due to parsing error: {uri} | Error: {e}")
        return None

def parse_vmess(uri: str) -> dict | None:
    """Parses a VMess URI and converts it to a sing-box outbound dictionary."""
    try:
        if not uri.startswith("vmess://"): return None
        b64_data = uri.replace("vmess://", "")
        b64_data += "=" * (-len(b64_data) % 4)
        decoded_data = json.loads(base64.b64decode(b64_data).decode('utf-8'))
        tag = decoded_data.get("ps") or f"vmess-{decoded_data.get('add')}"
        config = {
            "type": "vmess", "tag": tag, "server": decoded_data.get("add"),
            "server_port": int(decoded_data.get("port")), "uuid": decoded_data.get("id"),
            "security": decoded_data.get("scy", "auto"), "alter_id": decoded_data.get("aid", 0),
        }
        if net := decoded_data.get("net"):
            transport_config = {"type": net}
            if net == 'ws':
                transport_config["path"] = decoded_data.get("path", "/")
                if host := decoded_data.get("host"):
                    transport_config["headers"] = {"Host": host}
            elif net == 'grpc':
                transport_config["service_name"] = decoded_data.get("path", "")
            config["transport"] = transport_config
        if decoded_data.get("tls") in ["tls", "reality"]:
            tls_config = {
                "enabled": True,
                "server_name": decoded_data.get("sni", decoded_data.get("host", decoded_data.get("add"))),
            }
            if fp := decoded_data.get("fp"):
                tls_config["utls"] = {"enabled": True, "fingerprint": fp}
            config["tls"] = tls_config
        return config
    except Exception as e:
        print(f"Skipping VMess URI due to parsing error: {uri} | Error: {e}")
        return None

def parse_trojan(uri: str) -> dict | None:
    """Parses a Trojan URI and converts it to a sing-box outbound dictionary."""
    try:
        parsed_url = urlparse(uri)
        if not all([parsed_url.scheme == 'trojan', parsed_url.username, parsed_url.hostname, parsed_url.port]):
            return None
        query_params = parse_qs(parsed_url.query)
        tag = unquote(parsed_url.fragment) if parsed_url.fragment else f"trojan-{parsed_url.hostname}"
        config = {
            "type": "trojan", "tag": tag, "server": parsed_url.hostname,
            "server_port": parsed_url.port, "password": parsed_url.username,
        }
        tls_config = {"enabled": True, "server_name": query_params.get('sni', [parsed_url.hostname])[0]}
        if query_params.get('allowInsecure', ['0'])[0] == '1':
            tls_config["insecure"] = True
        config["tls"] = tls_config
        return config
    except Exception as e:
        print(f"Skipping Trojan URI due to parsing error: {uri} | Error: {e}")
        return None

def parse_shadowsocks(uri: str) -> dict | None:
    """Parses a Shadowsocks (SS) URI and converts it to a sing-box outbound."""
    try:
        parsed_url = urlparse(uri)
        tag = unquote(parsed_url.fragment) if parsed_url.fragment else parsed_url.hostname
        method, password = None, None
        if parsed_url.username and parsed_url.password:
            method = unquote(parsed_url.username)
            password = unquote(parsed_url.password)
        elif parsed_url.username:
            try:
                b64_data = unquote(parsed_url.username)
                b64_data += "=" * (-len(b64_data) % 4)
                decoded_bytes = base64.b64decode(b64_data)
                parts = decoded_bytes.split(b':', 1)
                if len(parts) == 2:
                    method = parts[0].decode('utf-8')
                    password = parts[1].decode('utf-8', 'replace')
            except (binascii.Error, UnicodeDecodeError):
                method = "aes-256-gcm"
                password = unquote(parsed_url.username)
        if not method or not password:
            return None
        return {
            "type": "shadowsocks", "tag": tag, "server": parsed_url.hostname,
            "server_port": parsed_url.port, "method": method, "password": password
        }
    except Exception as e:
        print(f"Skipping Shadowsocks URI due to parsing error: {uri} | Error: {e}")
        return None

def parse_hysteria2(uri: str) -> dict | None:
    """Parses a Hysteria2 URI and converts it to a sing-box outbound."""
    try:
        if uri.startswith("hy2://"):
            uri = uri.replace("hy2://", "hysteria2://", 1)
        parsed_url = urlparse(uri)
        if not all([parsed_url.scheme == 'hysteria2', parsed_url.username, parsed_url.hostname, parsed_url.port]):
            return None
        query_params = parse_qs(parsed_url.query)
        tag = unquote(parsed_url.fragment) if parsed_url.fragment else parsed_url.hostname
        return {
            "type": "hysteria2", "tag": tag, "server": parsed_url.hostname,
            "server_port": parsed_url.port, "password": parsed_url.username,
            "tls": {
                "enabled": True, "server_name": query_params.get('sni', [parsed_url.hostname])[0],
                "insecure": query_params.get('insecure', ['0'])[0] == '1'
            }
        }
    except Exception as e:
        print(f"Skipping Hysteria2 URI due to parsing error: {uri} | Error: {e}")
        return None

def parse_tuic(uri: str) -> dict | None:
    """Parses a TUIC URI and converts it to a sing-box outbound."""
    try:
        parsed_url = urlparse(uri)
        if not all([parsed_url.scheme == 'tuic', parsed_url.username, parsed_url.hostname, parsed_url.port]):
            return None
        user_info = parsed_url.username.split(':', 1)
        uuid, password = user_info if len(user_info) == 2 else (user_info[0], "")
        query_params = parse_qs(parsed_url.query)
        tag = unquote(parsed_url.fragment) if parsed_url.fragment else parsed_url.hostname
        return {
            "type": "tuic", "tag": tag, "server": parsed_url.hostname,
            "server_port": parsed_url.port, "uuid": uuid, "password": password,
            "congestion_control": query_params.get('congestion_control', ['bbr'])[0],
            "udp_relay_mode": query_params.get('udp_relay_mode', ['native'])[0],
            "tls": {
                "enabled": True, "server_name": query_params.get('sni', [parsed_url.hostname])[0],
                "insecure": query_params.get('allow_insecure', ['0'])[0] == '1',
                "alpn": query_params.get('alpn', [])
            }
        }
    except Exception as e:
        print(f"Skipping TUIC URI due to parsing error: {uri} | Error: {e}")
        return None

def parse_juicity(uri: str) -> dict | None:
    """Parses a Juicity URI and converts it to a sing-box outbound."""
    try:
        parsed_url = urlparse(uri)
        if not all([parsed_url.scheme == 'juicity', parsed_url.username, parsed_url.hostname, parsed_url.port]):
            return None
        query_params = parse_qs(parsed_url.query)
        tag = unquote(parsed_url.fragment) if parsed_url.fragment else parsed_url.hostname
        return {
            "type": "juicity", "tag": tag, "server": parsed_url.hostname,
            "server_port": parsed_url.port, "uuid": parsed_url.username,
            "password": query_params.get('password', [""])[0]
        }
    except Exception as e:
        print(f"Skipping Juicity URI due to parsing error: {uri} | Error: {e}")
        return None


# --- DOWNLOADER SCRIPT ---

def create_full_config(outbounds: list) -> dict:
    """Wraps a list of outbound configurations in a complete sing-box config structure."""
    all_tags = [proxy["tag"] for proxy in outbounds]
    real_proxy_tags = [proxy["tag"] for proxy in outbounds if proxy.get("server") != "127.0.0.1"]
    return {
        "log": {"level": "info", "timestamp": True},
        "dns": {
            "servers": [
                {"tag": "dns_proxy", "address": "proxy://dns-out/dns-query", "detour": "PROXY"},
                {"tag": "dns_direct", "address": "https://1.1.1.1/dns-query", "detour": "DIRECT"},
                {"tag": "dns_block", "address": "rcode://success"}
            ]
        },
        "inbounds": [
            {
                "type": "tun", "interface_name": "tun0", "inet4_address": "172.19.0.1/30",
                "auto_route": True, "strict_route": True, "sniff": True
            }
        ],
        "outbounds": [
            {"type": "selector", "tag": "PROXY", "outbounds": ["AUTO-SELECT"] + all_tags, "default": "AUTO-SELECT"},
            {"type": "url-test", "tag": "AUTO-SELECT", "outbounds": real_proxy_tags, "url": "http://www.gstatic.com/generate_204"},
            *outbounds,
            {"type": "dns", "tag": "dns-out"},
            {"type": "direct", "tag": "DIRECT"},
            {"type": "block", "tag": "BLOCK"}
        ],
        "route": {
             "rules": [
                {"protocol": "dns", "outbound": "dns-out"},
                {"network": "udp", "port": 443, "outbound": "BLOCK"},
            ],
            "final": "PROXY"
        }
    }


def fetch_and_process(url, base_dir="."):
    """Fetches, decodes, parses, and saves a full sing-box config file."""
    if not url.startswith("http"):
        url = "https://" + url
    try:
        path = urlparse(url).path
        local_path = path.split('/main/')[-1]
        
        # Determine directory and filename, ensuring .txt extension
        if local_path.endswith('/mixed'):
            parts = local_path.split('/')
            directory = os.path.join(base_dir, *parts[:-1])
            filename = "mixed.txt" 
        else:
            parts = local_path.split('/')
            directory = os.path.join(base_dir, *parts[:-1])
            filename = parts[-1] + ".txt"

        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)

        print(f"Fetching and processing {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        raw_text = response.text.strip()
        
        try:
            decoded_text = base64.b64decode(raw_text).decode('utf-8')
            if any(proto in decoded_text for proto in ["vless://", "vmess://", "ss://", "trojan://", "tuic://", "hy2://", "hysteria2://", "juicity://"]):
                raw_text = decoded_text
                print(f"  -> Content was Base64 encoded, decoded successfully.")
        except (binascii.Error, UnicodeDecodeError):
            pass

        outbounds = []
        supported_protocols = {
            "vless://": parse_vless, "vmess://": parse_vmess, "trojan://": parse_trojan,
            "ss://": parse_shadowsocks, "hysteria2://": parse_hysteria2,
            "hy2://": parse_hysteria2, "tuic://": parse_tuic, "juicity://": parse_juicity,
        }
        for line in raw_text.splitlines():
            line = line.strip()
            if not line: continue
            for prefix, parser in supported_protocols.items():
                if line.startswith(prefix):
                    if parsed_config := parser(line):
                        outbounds.append(parsed_config)
                    break
        
        if outbounds:
            full_config_json = create_full_config(outbounds)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(full_config_json, f, indent=2, ensure_ascii=False)
            print(f"Successfully processed and saved to {filepath}")
        else:
            print(f"No valid configs found in {url}, skipping file creation.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"An error occurred for {url}: {e}")

# --- README GENERATION FUNCTIONS ---

def generate_simple_table(title, category_path, repo_url_raw, base_dir):
    """Generates a simple two-column Markdown table for a given category."""
    header = f"| **{title}** | **Subscription Link** |\n|:---:|:---:|\n"
    body = ""
    if os.path.isdir(category_path):
        for filename in sorted(os.listdir(category_path)):
            if filename.endswith(".txt"):
                name = os.path.splitext(filename)[0].replace('-', ' ').title()
                if name.lower() == 'mixed':
                    name = "Mixed Type Configurations"
                else:
                    name += " Configurations"
                
                relative_path = os.path.join(category_path.replace(base_dir, ''), filename).replace('\\', '/').lstrip('/')
                link = f"{repo_url_raw}/{base_dir}/{relative_path}"
                body += f"| **{name}** | [Link]({link}) |\n"
    return header + body + "\n"

def generate_country_table(countries_path, repo_url_raw, base_dir):
    """Generates the multi-column Markdown table for countries."""
    header = "| Code | Country | Link | Code | Country | Link |\n|:---:|:---:|:---:|:---:|:---:|:---:|\n"
    body_parts = []
    
    if os.path.isdir(countries_path):
        country_codes = sorted([d for d in os.listdir(countries_path) if os.path.isdir(os.path.join(countries_path, d))])
        
        for code in country_codes:
            # FIX: Use .lower() to match the lowercase keys in the COUNTRY_CODES dictionary.
            country_name = COUNTRY_CODES.get(code.lower(), code.upper())
            relative_path = os.path.join(countries_path.replace(base_dir, ''), code, 'mixed.txt').replace('\\', '/').lstrip('/')
            link = f"{repo_url_raw}/{base_dir}/{relative_path}"
            
            body_parts.append(f"| {code.upper()} | {country_name} | [Link]({link})")

    final_body = ""
    for i in range(0, len(body_parts), 2):
        final_body += body_parts[i]
        if i + 1 < len(body_parts):
            final_body += body_parts[i+1] + " |\n"
        else:
            final_body += " | | | |\n"
            
    return header + final_body + "\n"

def generate_readme(base_dir, repo_url_raw):
    """Generates the entire README.md file content."""
    print("Generating README.md...")
    
    readme_header = """# Automated Sing-Box Subscription Collector

This repository automatically fetches, categorizes, and compiles the latest server configurations from the public soroushmirzaei/telegram-configs-collector project.
All configurations are then made available as distinct subscription links compatible with Sing-Box, Nekobox, and other modern clients. This project is automated using GitHub Actions and updates every hour.

## How to Use a Subscription Link
To use these subscriptions, you need to copy the raw URL of a subscription file and add it to your client app (e.g., Sing-Box) as a "Remote Profile".

1.  Find the subscription you want in the tables below.
2.  Right-click on the link (e.g., on "Vless Configurations" or "Germany") and select "Copy Link Address".
3.  In the Sing-Box app, go to **Profiles** -> **New Profile** -> **Remote** and paste the copied URL.

## Main Subscription Link
This link contains all unique configurations from all sources combined into a single file. 
**Note:** A script to combine all configs is not included here, so this link is a placeholder.

- [**All Configs (Placeholder)**](https://example.com/all.txt)

## Categorized Subscription Links

To use a link, right-click on it and select **"Copy Link Address"**.
"""

    readme_footer = """
## Automation
This repository uses a GitHub Actions workflow to automatically update all subscription files at 10 minutes past every hour. This ensures the configurations are always fresh.

## Credits
This project would not be possible without the incredible work done by Soroush Mirzaei and the community contributors to the telegram-configs-collector repository.
"""

    protocols_table = "### Protocol Type Subscription Links\n" + generate_simple_table("Protocol Type", os.path.join(base_dir, "protocols"), repo_url_raw, base_dir)
    networks_table = "### Network Type Subscription Links\n" + generate_simple_table("Network Type", os.path.join(base_dir, "networks"), repo_url_raw, base_dir)
    security_table = "### Security Type Subscription Links\n" + generate_simple_table("Security Type", os.path.join(base_dir, "security"), repo_url_raw, base_dir)
    layers_table = "### Internet Protocol Type Subscription Links\n" + generate_simple_table("Internet Protocol", os.path.join(base_dir, "layers"), repo_url_raw, base_dir)
    countries_table = "### Country Subscription Links\n" + generate_country_table(os.path.join(base_dir, "countries"), repo_url_raw, base_dir)

    # FIX: Combine all parts into a single f-string for better style and readability.
    full_readme_content = f"""{readme_header}
{protocols_table}
{networks_table}
{security_table}
{layers_table}
{countries_table}
{readme_footer}
"""

    with open("README.md", 'w', encoding='utf-8') as f:
        f.write(full_readme_content)
    print("Successfully generated README.md")


if __name__ == "__main__":
    REPO_URL_RAW = "https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main"
    OUTPUT_DIR = "collected_configs"

    urls_text = """
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/juicity
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/hysteria
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/tuic
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/reality
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vmess
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/trojan
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/shadowsocks
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/splitted/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/networks/grpc
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/networks/http
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/networks/ws
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/networks/tcp
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/security/tls
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/security/non-tls
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/layers/ipv4
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/layers/ipv6
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/al/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ar/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/am/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/au/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/at/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/bh/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/be/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/bo/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ba/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/br/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/bg/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ca/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/cl/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/cn/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/co/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/cr/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/hr/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/cy/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/cz/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/dk/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ec/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ee/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/fi/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/fr/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/de/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/gi/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/gr/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/gt/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/hk/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/is/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/in/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/id/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ir/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ie/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/il/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/it/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/jp/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/jo/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/kz/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/kr/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/lv/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/lt/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/lu/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/my/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/mt/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/mu/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/mx/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/md/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ma/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/mm/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/nl/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/nz/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ng/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/mk/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/no/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/na/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/om/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/pk/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/py/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/pe/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ph/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/pl/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/pt/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/pr/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ro/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ru/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/sa/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/rs/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/sc/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/sg/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/sk/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/si/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/za/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/es/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/se/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ch/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/tw/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/th/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/tr/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ua/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ae/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/gb/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/us/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/vn/mixed
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/vg/mixed
    """
    
    all_urls = re.findall(r'https?://[^\s<>"\']+', urls_text)

    for url in all_urls:
        fetch_and_process(url, base_dir=OUTPUT_DIR)

    generate_readme(OUTPUT_DIR, REPO_URL_RAW)

    print("\nAll tasks completed.")
