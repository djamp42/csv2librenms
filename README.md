# csv2librenms

CSV bulk importer for LibreNMS, import devices as SNMP or PING only.

This will add a device for each row in data/bulkimport.csv.

Please add your LibreNMS API key in the config.py file. You can generate
them via the LibreNMS webgui. 

**Direction: python ./bulkadd.py**

---
### CSV File Example

#### SNMP Settings
- **Hostname**: IP/Hostname of device you want to add
- **ro**: SNMP read only community string of device
#### Ping Settings
- **sysname**: sysname of device
- **os**: this is the os name in librenms, you can get a list of os
  names from
  [LibreNMS OS definitions](https://github.com/librenms/librenms/tree/master/includes/definitions)
- **hardware**: hardware description of device
- **location_id**: In order to add a syslocation to PING only devices,
  you need to first create a device in that location manually with the
  LibreNMS webgui. To get the Location ID, in the webgui go to Geo
  Locations -> All Locations -> Click on the location, your url should
  contain the Location ID: http://#.#.#.#/devices/location=213 (213 is
  the location ID)

