#!/usr/bin/python
import requests
import json
import config

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

def device_update(update_request):
    api_url = "http://{}/api/v0/devices".format(config.librenms_ipaddress)
    r = requests.patch(api_url, json=update_request, headers=request_headers)
    print(r.text)


def bulkaddping():
    df = pd.read_csv("data/bulkadd.csv")

    for index, row in df.iterrows():
        # Create JSON format data for API delivery
        device = {
            "hostname":row['hostname'],
            "sysName":row['sysname'],
            "hardware":row['hardware'],
            "force_add":"true",
            "snmp_disable":"true"
                 }
        # Add device to LibreNMS.
        device_add(device)

        # In order to add a location to PING only devices, you need to first create a device in that
        # location manually with the LibreNMS webgui. To get the Location ID, in the webgui go to
        # Geo Locations -> All Locations -> Click on the location, your url should contain the Location ID:
        # http://#.#.#.#/devices/location=213  (213 is the location ID)

        if row['location_id'] == "":
            continue
        else:
            location = {
                "field":["location_id","override_sysLocation"],
                "data":[row['location_id'],row['override_sysLocation']]
                        }
            device_update(location)


def bulkaddsnmpv2():
    df = pd.read_csv("data/bulkadd.csv")
    for index, row in df.iterrows():
        # Add Device to LibreNMS
        add_device = {
            "hostname":row['hostname'],
            "community":row['ro'],
            "version":"v2c"
            }
        device_add(add_device)