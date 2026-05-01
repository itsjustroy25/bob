# Cloudflare Tunnel Setup for itsjustbob.chat

## Prerequisites
- Domain registered at Namecheap (itsjustbob.chat)
- Cloudflare account
- Flask running on garage machine port 5000

## Step 1 - Move DNS to Cloudflare
1. Add itsjustbob.chat to Cloudflare account
2. Cloudflare scans existing DNS records
3. At Namecheap: Domain List → Manage → Nameservers →
   Custom DNS → enter Cloudflare nameservers:
   - augustus.ns.cloudflare.com
   - colette.ns.cloudflare.com
4. Wait for propagation (5-30 minutes)

## Step 2 - Install cloudflared on garage machine
``bash
curl -L https://pkg.cloudflare.com/cloudflare-main.gpg \
  | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] \
  https://pkg.cloudflare.com/cloudflared any main' \
  | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update
sudo apt install cloudflared
``

## Step 3 - Authenticate cloudflared
``bash
cloudflared tunnel login
``
Opens browser to authorize. Select itsjustbob.chat.

## Step 4 - Create tunnel
``bash
cloudflared tunnel create bob
``
Credentials written to ~/.cloudflared/<uuid>.json. Keep secret.

## Step 5 - Route domain to tunnel
``bash
cloudflared tunnel route dns bob itsjustbob.chat
``
Note: Delete any existing CNAME records in Cloudflare DNS first.

## Step 6 - Run tunnel
``bash
cloudflared tunnel run --url http://localhost:5000 bob &
``

## Notes
- Cloudflare provides free SSL automatically
- No firewall holes needed - tunnel is outbound only
- If containers restart, cloudflared needs restart too
- Order of operations: restart containers THEN restart cloudflared
- Bob's brain stays local, only web traffic goes through Cloudflare

## Restart cloudflared
``bash
pkill cloudflared
cloudflared tunnel run --url http://localhost:5000 bob &
```
