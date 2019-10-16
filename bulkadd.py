#!/usr/bin/python
import config
import math
import requests
import pandas as pd

# Setup Requests Headers
request_headers = {"Content-Type": "application/json",
                   "Accept-Language": "en-US,en;q=0.5",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "X-Auth-Token": config.librenms_apikey,
                   "Connection": "keep-alive"
                   }

def device_add(add_request):
    api_url = "http://{}/api/v0/devices".format(config.librenms_ipaddress)
    r = requests.post(api_url, json=add_request, headers=request_headers)
    print(r.text)

def device_update(hostname, update_request):
    api_url = "http://{}/api/v0/devices/{}".format(config.librenms_ipaddress, hostname)
    r = requests.patch(api_url, json=update_request, headers=request_headers)
    print(r.text)

# Read CSV file
try:
    df = pd.read_csv("data/bulkadd.csv")
except FileNotFoundError:
    print("ERROR: data/bulkadd.csv missing")
    quit()

for index, row in df.iterrows():
    try:
        if math.isnan(row['ro']):
            # Add to Librenms as PING only Device
            # Create JSON data for API delivery
            device = {"hostname":row['hostname'],
                      "sysName":row['sysname'],
                      "hardware":row['hardware'],
                      "force_add":"true",
                      "snmp_disable":"true"
                      }
            # Add device to LibreNMS.
            device_add(device)

            # Update device with OS Type if provided
            try:
                if math.isnan(row['os']):
                    pass
            except:
                ostype = {"field": ["os"],
                          "data": [row['os']]
                          }
                device_update(row['hostname'], ostype)


            # Update device with syslocation if provided
            if math.isnan(row['location_id']):
                pass
            else:
                location = {"field": ["location_id", "override_sysLocation"],
                            "data": [row['location_id'], 1]
                            }
                device_update(row['hostname'], location)

    except:
        # Add Device to LibreNMS via SNMP
        add_device = {
            "hostname":row['hostname'],
            "community":row['ro'],
            "version":"v2c"
            }
        device_add(add_device)
quit()