#!/bin/bash

LOG="/home/rleach/bob/watchdog.log"
STARTALL="/home/rleach/bob/startall.sh"
MAX_DOCKER_WAIT=90

log() {
	echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG
}

check_bob() {
	response=$(curl -s -o /dev/null -w "%{http_code}" \
		--max-time 10 http://localhost:80)
			echo $response
		}

	check_docker() {
		docker ps > /dev/null 2>&1
		echo $?
	}

reboot_windows() {
	log "CRITICAL: Docker dead. Rebooting Windows..."
	/mnt/c/Windows/System32/shutdown.exe /r /t 30 /c "Bob watchdog initiated reboot - Docker failure"
}

while true; do
	status=$(check_bob)

	if [ "$status" != "200" ]; then
		log "Bob is down (HTTP $status). Investigating..."

		# Check Docker first
		if ! docker ps > /dev/null 2>&1; then
			log "Docker is dead. No point trying to restart containers."
			reboot_windows
			# Sleep long enough for reboot to happen
			sleep 300
			continue
		fi

																    # Docker is alive, just containers died
																    log "Docker running but Bob is down. Restarting services..."
																    $STARTALL >> $LOG 2>&1

																    # Wait and verify
																    sleep 120
																    status=$(check_bob)

																    if [ "$status" == "200" ]; then
																	    log "Bob recovered successfully."
																    else
																	    log "Bob recovery failed after restart. Rebooting Windows..."
																	    reboot_windows
																	    sleep 300
																    fi
	fi

	sleep 300
done
