import os
import requests
from urllib.parse import urlparse

def clean_urls(text):
    """Cleans and separates concatenated URLs."""
    return text.replace('https://', ' https://').split()

def fetch_and_save(url, base_dir="."):
    """
    Fetches content from a URL and saves it to a local file,
    mimicking the repository's directory structure.
    """
    if not url.startswith("http"):
        url = "https://" + url

    try:
        # Parse the URL to get the path
        path = urlparse(url).path
        # Extract the relevant part of the path for the local file structure
        local_path = path.split('/main/')[-1]

        # Define the local directory and filename
        if local_path.endswith('/mixed'):
            # For country-specific mixed files
            parts = local_path.split('/')
            directory = os.path.join(base_dir, *parts[:-1])
            filename = "mixed.txt"
        else:
            # For other files
            parts = local_path.split('/')
            directory = os.path.join(base_dir, *parts[:-1])
            filename = parts[-1] + ".txt"

        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Define the full local filepath
        filepath = os.path.join(directory, filename)

        # Fetch the content from the URL
        print(f"Fetching {url}...")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Save the content to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)

        print(f"Successfully saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"An error occurred for {url}: {e}")


if __name__ == "__main__":
    # Raw text containing all the URLs
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

    # Clean the URLs
    all_urls = clean_urls(urls_text)

    # Process each URL
    for url in all_urls:
        fetch_and_save(url, base_dir="collected_configs")

    print("\nAll tasks completed.")
