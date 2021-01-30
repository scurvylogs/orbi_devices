# orbi_devices

### Pulls device list from Orbi mesh router and posts in Splunk HEC

* Python 3.6+
* Libraries required
  * requests==2.25.1
  * urllib3==1.26.3
* Usage with Splunk HEC: python get_connected_devices.py
* Usage without Splunk HEC: python get_connected_devices_no_splunk.py

### Credential files required:
* .splunk - splunk HEC auth token (if Splunk is used)
* .orbi - administrator username and password

### Notes:
* Tested on router firmware version V2.5.2.4
* Most likely will not work in older versions and likely to break in newer releases
* Report issues with the code in the github repository
* GNU GPL v3 license