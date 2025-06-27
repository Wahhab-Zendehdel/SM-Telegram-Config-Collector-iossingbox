Automated Sing-Box Subscription Collector
This repository automatically fetches, categorizes, and compiles the latest server configurations from the public soroushmirzaei/telegram-configs-collector project.

All configurations are then made available as distinct subscription links compatible with Sing-Box, Nekobox, and other modern clients. This project is automated using GitHub Actions and updates every hour.

How to Use a Subscription Link
To use these subscriptions, you need to copy the raw URL of a subscription file and add it to your client app (e.g., Sing-Box) as a "Remote Profile".

Navigate to the subscriptions folder in this repository.

Choose a category folder (like country or protocol) and click on the .txt file you want. For example, to get all VLESS configs, go to protocol/vless.txt.

On the file page, click the "Raw" button in the top right corner.

Copy the URL from your browser's address bar. This is your subscription link.

In the Sing-Box app, go to Profiles -> New Profile -> Remote and paste the copied URL.

Main Subscription Link
This link contains all unique configurations from all sources combined into a single file.

All Configs: https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPOSITORY/main/subscriptions/All_Configs.txt

Categorized Subscriptions
You can also use more specific subscriptions based on your needs. All links can be found inside the subscriptions directory of this repository.

By Protocol
Browse Protocol Subscriptions

Examples: vless.txt, trojan.txt, ss.txt

By Country
Browse Country Subscriptions

Examples: us.txt (United States), de.txt (Germany), jp.txt (Japan)

By Network Type
Browse Network Subscriptions

Examples: ws.txt (WebSocket), grpc.txt, tcp.txt

By Security Type
Browse Security Subscriptions

Examples: tls.txt, reality.txt, none.txt

By IP Version
Browse IP Version Subscriptions

Examples: ipv4.txt, ipv6.txt

Automation
This repository uses a GitHub Actions workflow to automatically update all subscription files at 10 minutes past every hour. This ensures the configurations are always fresh.

Credits
This project would not be possible without the incredible work done by Soroush Mirzaei and the community contributors to the telegram-configs-collector repository.
