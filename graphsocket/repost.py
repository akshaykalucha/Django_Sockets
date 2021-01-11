#!/usr/bin/env python3

"""Pick server and start connection with VPNGate (http://www.vpngate.net/en/)"""

import requests
import os
import sys
import tempfile
import subprocess
import base64
import time

__author__ = "Andrea Lazzarotto"
__copyright__ = "Copyright 2014+, Andrea Lazzarotto"
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Andrea Lazzarotto"
__email__ = "andrea.lazzarotto@gmail.com"


if len(sys.argv) != 2:
    print("usage: " + sys.argv[0] + " [country name | country code]")
    exit(1)
country = sys.argv[1]

if len(country) == 2:
    i = 6  # short name for country
elif len(country) > 2:
    i = 5  # long name for country
else:
    print("Country is too short!")
    exit(1)

try:
    vpn_data = requests.get("http://www.vpngate.net/api/iphone/").text.replace("\r", "")
    servers = [line.split(",") for line in vpn_data.split("\n")]
    labels = servers[1]
    labels[0] = labels[0][1:]
    servers = [s for s in servers[2:] if len(s) > 1]
except BaseException:
    print("Cannot get VPN servers data")
    exit(1)