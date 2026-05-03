# Cloudflare Tunnel Setup for itsjustbob.chat

## Prerequisites
- Domain registered at Namecheap (itsjustbob.chat)
- Cloudflare account
- Flask running on garage machine port 80 (via Nginx)

## Step 1 - Move DNS to Cloudflare
1. Add itsjustbob.chat to Cloudflare account
2. Cloudflare scans existing DNS records
3. At Namecheap: Domain List → Manage → Nameservers → 
   Custom DNS → enter Cloudflare nameservers:
   - augustus.ns.cloudflare.com
   - colette.ns.cloudflare.com
4. Wait for propagation (5-30 minutes)

## Step 2 - Install cloudflared on garage machine
```bash
curl -L https://pkg.cloudflare.com/cloudflare-main.gpg \
  | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] \
  https://pkg.cloudflare.com/cloudflared any main' \
  | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update
sudo apt install cloudflared
```

## Step 3 - Authenticate cloudflared
```bash
cloudflared tunnel login
```
Opens browser to authorize. Select itsjustbob.chat.

## Step 4 - Create tunnel
```bash
cloudflared tunnel create bob
```
Credentials written to ~/.cloudflared/<uuid>.json. Keep secret.
Note the UUID -- you will need it for config.yml.

## Step 5 - Route domain to tunnel
```bash
cloudflared tunnel route dns bob itsjustbob.chat
```
Note: Delete any existing CNAME records in Cloudflare DNS first.

## Step 6 - Create config.yml
Create ~/.cloudflared/config.yml:

```yaml
tunnel: YOUR-TUNNEL-UUID
credentials-file: /home/USERNAME/.cloudflared/YOUR-TUNNEL-UUID.json
ingress:
  - hostname: itsjustbob.chat
    service: http://localhost:80
  - service: http_status:404
```

Note: tunnel field requires the UUID not the tunnel name "bob".

## Step 7 - Install as a Service (Survives Reboots)
```bash
sudo cloudflared --config /home/USERNAME/.cloudflared/config.yml service install
```

## Step 8 - Start the Service
```bash
sudo service cloudflared start
sudo service cloudflared status
```

## Managing the Service
```bash
# Start
sudo service cloudflared start

# Stop
sudo service cloudflared stop

# Restart
sudo service cloudflared restart

# Status
sudo service cloudflared status

# Kill manual instance if running alongside service
sudo pkill cloudflared
sudo service cloudflared start
```

## Notes
- Cloudflare provides free SSL automatically
- No firewall holes needed -- tunnel is outbound only
- Service survives reboots AND SSH disconnects
- No need for nohup or & anymore
- Uses SysV on WSL (not systemd)
- Bob's brain stays local, only web traffic goes through Cloudflare
- Order of operations when restarting containers:
  1. Restart containers
  2. Restart cloudflared service if needed

## Architecture
Browser -> HTTPS -> Cloudflare -> encrypted tunnel ->
cloudflared service -> Nginx :80 -> Flask :5000 -> Ollama :11434
