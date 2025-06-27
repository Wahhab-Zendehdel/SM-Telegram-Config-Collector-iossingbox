# Automated Sing-Box Subscription Collector

This repository automatically fetches, categorizes, and compiles the latest server configurations from the public soroushmirzaei/telegram-configs-collector project.
All configurations are then made available as distinct subscription links compatible with Sing-Box, Nekobox, and other modern clients. This project is automated using GitHub Actions and updates every hour.

## How to Use a Subscription Link
To use these subscriptions, you need to copy the raw URL of a subscription file and add it to your client app (e.g., Sing-Box) as a "Remote Profile".

1.  Find the subscription you want in the tables below.
2.  Right-click on the link (e.g., on "VLESS" or "Germany (DE)") and select "Copy Link Address".
3.  In the Sing-Box app, go to **Profiles** -> **New Profile** -> **Remote** and paste the copied URL.

## Main Subscription Link
This link contains all unique configurations from all sources combined into a single file.

- [**All Configs**](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/All_Configs_Subscription.txt)

## Categorized Subscription Links

To use a link, right-click on it and select **"Copy Link Address"**.

### Protocol Type Subscription Links

| **Protocol Type** | **Subscription Link** |
|:---:|:---:|
| **Juicity Configurations** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/protocols/juicity.txt) |
| **Hysteria Configurations** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/protocols/hysteria.txt) |
| **Tuic Configurations** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/protocols/tuic.txt) |
| **Reality Configurations** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/protocols/reality.txt) |
| **Vless Configurations** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/protocols/vless.txt) |
| **Vmess Configurations** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/protocols/vmess.txt) |
| **Trojan Configurations** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/protocols/trojan.txt) |
| **Shadowsocks Configurations** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/protocols/shadowsocks.txt) |
| **Mixed Type Configurations** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/splitted/mixed.txt) |

### Network Type Subscription Links

| **Network Type** | **Subscription Link** |
|:---:|:---:|
| **gRPC** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/networks/grpc.txt) |
| **HTTP** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/networks/http.txt) |
| **WebSocket** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/networks/ws.txt) |
| **TCP** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/networks/tcp.txt) |

### Security Type Subscription Links

| **Security Type** | **Subscription Link** |
|:---:|:---:|
| **TLS** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/security/tls.txt) |
| **Non-TLS** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/security/non-tls.txt) |

### Internet Protocol Type Subscription Links

| **Internet Protocol** | **Subscription Link** |
|:---:|:---:|
| **IPv4** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/layers/ipv4.txt) |
| **IPv6** | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/layers/ipv6.txt) |

### Country Subscription Links

| Code | Country | Link | Code | Country | Link |
|:---:|:---:|:---:|:---:|:---:|:---:|
| AL | Albania | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/al/mixed.txt) | AR | Argentina | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ar/mixed.txt) |
| AM | Armenia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/am/mixed.txt) | AU | Australia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/au/mixed.txt) |
| AT | Austria | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/at/mixed.txt) | BH | Bahrain | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/bh/mixed.txt) |
| BE | Belgium | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/be/mixed.txt) | BO | Bolivia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/bo/mixed.txt) |
| BA | Bosnia & Herz. | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ba/mixed.txt) | BR | Brazil | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/br/mixed.txt) |
| BG | Bulgaria | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/bg/mixed.txt) | CA | Canada | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ca/mixed.txt) |
| CL | Chile | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/cl/mixed.txt) | CN | China | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/cn/mixed.txt) |
| CO | Colombia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/co/mixed.txt) | CR | Costa Rica | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/cr/mixed.txt) |
| HR | Croatia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/hr/mixed.txt) | CY | Cyprus | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/cy/mixed.txt) |
| CZ | Czechia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/cz/mixed.txt) | DK | Denmark | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/dk/mixed.txt) |
| EC | Ecuador | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ec/mixed.txt) | EE | Estonia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ee/mixed.txt) |
| FI | Finland | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/fi/mixed.txt) | FR | France | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/fr/mixed.txt) |
| DE | Germany | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/de/mixed.txt) | GI | Gibraltar | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/gi/mixed.txt) |
| GR | Greece | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/gr/mixed.txt) | GT | Guatemala | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/gt/mixed.txt) |
| HK | Hong Kong | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/hk/mixed.txt) | IS | Iceland | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/is/mixed.txt) |
| IN | India | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/in/mixed.txt) | ID | Indonesia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/id/mixed.txt) |
| IR | Iran | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ir/mixed.txt) | IE | Ireland | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ie/mixed.txt) |
| IL | Israel | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/il/mixed.txt) | IT | Italy | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/it/mixed.txt) |
| JP | Japan | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/jp/mixed.txt) | JO | Jordan | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/jo/mixed.txt) |
| KZ | Kazakhstan | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/kz/mixed.txt) | KR | Korea | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/kr/mixed.txt) |
| LV | Latvia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/lv/mixed.txt) | LT | Lithuania | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/lt/mixed.txt) |
| LU | Luxembourg | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/lu/mixed.txt) | MY | Malaysia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/my/mixed.txt) |
| MT | Malta | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/mt/mixed.txt) | MU | Mauritius | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/mu/mixed.txt) |
| MX | Mexico | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/mx/mixed.txt) | MD | Moldova | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/md/mixed.txt) |
| MA | Morocco | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ma/mixed.txt) | MM | Myanmar | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/mm/mixed.txt) |
| NL | Netherlands | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/nl/mixed.txt) | NZ | New Zealand | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/nz/mixed.txt) |
| NG | Nigeria | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ng/mixed.txt) | MK | North Macedonia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/mk/mixed.txt) |
| NO | Norway | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/no/mixed.txt) | NA | Not Available | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/na/mixed.txt) |
| OM | Oman | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/om/mixed.txt) | PK | Pakistan | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/pk/mixed.txt) |
| PY | Paraguay | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/py/mixed.txt) | PE | Peru | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/pe/mixed.txt) |
| PH | Philippines | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ph/mixed.txt) | PL | Poland | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/pl/mixed.txt) |
| PT | Portugal | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/pt/mixed.txt) | PR | Puerto Rico | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/pr/mixed.txt) |
| RO | Romania | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ro/mixed.txt) | RU | Russia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ru/mixed.txt) |
| SA | Saudi Arabia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/sa/mixed.txt) | RS | Serbia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/rs/mixed.txt) |
| SC | Seychelles | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/sc/mixed.txt) | SG | Singapore | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/sg/mixed.txt) |
| SK | Slovakia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/sk/mixed.txt) | SI | Slovenia | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/si/mixed.txt) |
| ZA | South Africa | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/za/mixed.txt) | ES | Spain | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/es/mixed.txt) |
| SE | Sweden | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/se/mixed.txt) | CH | Switzerland | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ch/mixed.txt) |
| TW | Taiwan | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/tw/mixed.txt) | TH | Thailand | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/th/mixed.txt) |
| TR | Türkiye | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/tr/mixed.txt) | UA | Ukraine | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ua/mixed.txt) |
| AE | UAE | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/ae/mixed.txt) | GB | UK | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/gb/mixed.txt) |
| US | United States | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/us/mixed.txt) | VN | Viet Nam | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/vn/mixed.txt) |
| VG | Virgin Islands | [Link](https://raw.githubusercontent.com/Wahhab-Zendehdel/SM-Telegram-Config-Collector-iossingbox/main/collected_configs/countries/vg/mixed.txt) | | | |

## Automation
This repository uses a GitHub Actions workflow to automatically update all subscription files at 10 minutes past every hour. This ensures the configurations are always fresh.

## Credits
This project would not be possible without the incredible work done by Soroush Mirzaei and the community contributors to the telegram-configs-collector repository.
