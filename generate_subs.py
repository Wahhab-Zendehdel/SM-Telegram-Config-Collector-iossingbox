import os
import re
import requests
import json
from urllib.parse import urlparse, parse_qs, unquote
import base64
import binascii

# --- CONFIG PARSING FUNCTIONS ---

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
        
        decoded_part = ""
        if parsed_url.username and not parsed_url.password: # Base64 format: ss://<base64>#tag
            b64_data = parsed_url.username
            b64_data += "=" * (-len(b64_data) % 4)
            decoded_part = base64.b64decode(b64_data).decode('utf-8')
        elif parsed_url.username and parsed_url.password: # Standard format: ss://<method>:<pass>@<host>:<port>
            decoded_part = f"{parsed_url.username}:{parsed_url.password}"

        match = re.match(r'([^:]+):(.+)', decoded_part)
        if not match: return None
        method, password = match.groups()

        return {
            "type": "shadowsocks",
            "tag": tag,
            "server": parsed_url.hostname,
            "server_port": parsed_url.port,
            "method": method,
            "password": password
        }
    except Exception as e:
        print(f"Skipping Shadowsocks URI due to parsing error: {uri} | Error: {e}")
        return None

def parse_hysteria2(uri: str) -> dict | None:
    """Parses a Hysteria2 URI and converts it to a sing-box outbound."""
    try:
        parsed_url = urlparse(uri)
        if not all([parsed_url.scheme == 'hysteria2', parsed_url.username, parsed_url.hostname, parsed_url.port]):
            return None
        query_params = parse_qs(parsed_url.query)
        tag = unquote(parsed_url.fragment) if parsed_url.fragment else parsed_url.hostname
        config = {
            "type": "hysteria2",
            "tag": tag,
            "server": parsed_url.hostname,
            "server_port": parsed_url.port,
            "password": parsed_url.username,
            "tls": {
                "enabled": True,
                "server_name": query_params.get('sni', [parsed_url.hostname])[0],
                "insecure": query_params.get('insecure', ['0'])[0] == '1'
            }
        }
        return config
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
        
        config = {
            "type": "tuic",
            "tag": tag,
            "server": parsed_url.hostname,
            "server_port": parsed_url.port,
            "uuid": uuid,
            "password": password,
            "congestion_control": query_params.get('congestion_control', ['bbr'])[0],
            "udp_relay_mode": query_params.get('udp_relay_mode', ['native'])[0],
            "tls": {
                "enabled": True,
                "server_name": query_params.get('sni', [parsed_url.hostname])[0],
                "insecure": query_params.get('allow_insecure', ['0'])[0] == '1',
                "alpn": query_params.get('alpn', [])
            }
        }
        return config
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
            "type": "juicity",
            "tag": tag,
            "server": parsed_url.hostname,
            "server_port": parsed_url.port,
            "uuid": parsed_url.username,
            "password": query_params.get('password', [""])[0]
        }
    except Exception as e:
        print(f"Skipping Juicity URI due to parsing error: {uri} | Error: {e}")
        return None


# --- MODIFIED DOWNLOADER SCRIPT ---

def clean_urls(text):
    """Cleans and separates concatenated URLs."""
    return text.replace('https://', ' https://').split()

def fetch_and_process(url, base_dir="."):
    """Fetches content, decodes if Base64, parses links, and saves as JSON."""
    if not url.startswith("http"):
        url = "https://" + url
    try:
        path = urlparse(url).path
        local_path = path.split('/main/')[-1]
        if local_path.endswith('/mixed'):
            parts = local_path.split('/')
            directory = os.path.join(base_dir, *parts[:-1])
            filename = "mixed.json"
        else:
            parts = local_path.split('/')
            directory = os.path.join(base_dir, *parts[:-1])
            filename = parts[-1] + ".json"
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)

        print(f"Fetching and processing {url}...")
        response = requests.get(url)
        response.raise_for_status()

        raw_text = response.text.strip()

        # --- NEW DECODING LOGIC ---
        # Attempts to decode the fetched content if it appears to be Base64.
        try:
            decoded_text = base64.b64decode(raw_text).decode('utf-8')
            # If the decoded text contains protocol prefixes, it's very likely a valid sub.
            if any(proto in decoded_text for proto in ["vless://", "vmess://", "ss://", "trojan://", "tuic://"]):
                 raw_text = decoded_text
                 print(f"    -> Content was Base64 encoded, decoded successfully.")
        except (binascii.Error, UnicodeDecodeError):
            # It's not Base64 or failed to decode, so process it as plain text.
            pass
        # --- END OF NEW LOGIC ---

        outbounds = []
        # --- ADDED NEW PROTOCOLS ---
        supported_protocols = {
            "vless://": parse_vless,
            "vmess://": parse_vmess,
            "trojan://": parse_trojan,
            "ss://": parse_shadowsocks,
            "hysteria2://": parse_hysteria2,
            "tuic://": parse_tuic,
            "juicity://": parse_juicity,
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
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(outbounds, f, indent=2, ensure_ascii=False)
            print(f"Successfully processed and saved to {filepath}")
        else:
            print(f"No valid configs found in {url}, skipping file creation.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"An error occurred for {url}: {e}")


if __name__ == "__main__":
    urls_text = """
    Protocol Type Mixed Configurations:
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/juicityhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/hysteriahttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/tuichttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/realityhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vlesshttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vmesshttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/trojanhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/shadowsockshttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/splitted/mixed

    Network Type Mixed Configurations:
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/networks/grpchttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/networks/httphttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/networks/wshttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/networks/tcp

    Security Type Mixed Configurations:
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/security/tlshttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/security/non-tls

    Internet Protocol Type Mixed Configurations:
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/layers/ipv4https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/layers/ipv6

    Country Mixed Configurations:
    https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/al/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ar/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/am/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/au/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/at/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/bh/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/be/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/bo/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ba/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/br/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/bg/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ca/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/cl/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/cn/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/co/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/cr/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/hr/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/cy/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/cz/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/dk/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ec/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ee/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/fi/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/fr/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/de/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/gi/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/gr/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/gt/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/hk/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/is/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/in/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/id/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ir/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ie/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/il/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/it/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/jp/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/jo/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/kz/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/kr/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/lv/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/lt/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/lu/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/my/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/mt/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/mu/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/mx/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/md/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ma/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/mm/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/nl/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/nz/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ng/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/mk/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/no/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/na/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/om/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/pk/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/py/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/pe/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ph/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/pl/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/pt/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/pr/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ro/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ru/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/sa/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/rs/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/sc/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/sg/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/sk/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/si/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/za/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/es/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/se/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ch/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/tw/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/th/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/tr/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ua/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ae/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/gb/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/us/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/vn/mixedhttps://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/vg/mixed
    """
    all_urls = clean_urls(urls_text)

    for url in all_urls:
        fetch_and_process(url, base_dir="collected_configs")

    print("\nAll tasks completed.")
