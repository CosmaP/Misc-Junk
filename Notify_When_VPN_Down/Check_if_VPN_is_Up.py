#!/usr/bin/env python

import psutil
from win10toast import ToastNotifier
import time

def check_vpn_status():
    while True:
        # Check if the VPN connection is active
        vpn_active = False
        for conn in psutil.net_connections():
            if conn.status == 'ESTABLISHED' and 'vpn' in conn.raddr.ip.lower():
                vpn_active = True
                break

        # If VPN is not active, show a notification
        if not vpn_active:
            toaster = ToastNotifier()
            toaster.show_toast("VPN Disconnected", "Your Microsoft VPN has been disconnected!", duration=10)

        time.sleep(60)  # Check every 60 seconds

# Start checking VPN status
check_vpn_status()
