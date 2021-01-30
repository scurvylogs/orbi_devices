# requests==2.25.1
import requests
from requests.auth import HTTPBasicAuth
import time
# urllib3==1.26.3
import urllib3
import json


def get_connected_devices(url, admin, passwd):
    r = requests.get(url, auth=HTTPBasicAuth(admin, passwd), verify=False)
    devices = r.text.splitlines()[1][7:]
    return r.status_code, devices


def post_splunk_http_collector(url, token, json_text):
    epoch = str(int(time.time()))
    json_text = '{"time": "' + epoch + '", "event": ' + json_text + '}'
    blob_json = json.loads(json_text)
    splunk_header = json.loads('{"Authorization" : "Splunk ' + token + '"}')
    result = requests.post(url=url, headers=splunk_header, json=blob_json, verify=False)
    return result


if __name__ == '__main__':
    print('STATUS: Starting execution.')
    urllib3.disable_warnings()
    # Preparing to call get_connected_devices
    # IP address for the Orbi router
    orbi_router_ip = '172.16.0.1'
    # URL to query connected devices
    orbi_url = 'https://'+orbi_router_ip+'/DEV_device_info.htm'
    # retrieve Orbi router admin and password from file .orbi
    with open('.orbi') as f:
        lines = f.readlines()
    f.close()
    admin_user = lines[0].rstrip('\n')
    admin_password = lines[1].rstrip('\n')
    http_response, devices_text = get_connected_devices(orbi_url, admin_user, admin_password)
    # The Orbi router sometimes does not honor the request and returns 401
    # just try again and will succeed eventually
    if http_response != 200:
        print(f'ERROR: Failed to retrieve devices from Orbi router: response code {http_response}.')
        print('ERROR: Verify settings and hardware.')
    else:
        print('SUCCESS: Devices connected to Orbi mesh:')
        print(json.dumps(json.loads(devices_text), sort_keys=True, indent=4))
    # If you are not using Splunk, just comment out or remove the if block
    if http_response == 200:
        # Send results to Splunk HTTP event collector with event type = _json
        print('STATUS: Sending to Splunk HTTP event collector.')
        splunk_host = 'splunk:8088'
        # URL of the Splunk HTTP event collector
        splunk_url = 'https://' + splunk_host + '/services/collector/event'
        # Read Splunk HTTP event collector auth token from file .splunk
        # Token in file is an example from
        # https://docs.splunk.com/Documentation/Splunk/8.1.1/Data/HTTPEventCollectortokenmanagement
        splunk_token_file = '.splunk'
        with open('.splunk') as f:
            lines = f.readlines()
        f.close()
        splunk_token = lines[0].rstrip('\n')
        response = post_splunk_http_collector(splunk_url, splunk_token, devices_text)
        if response.status_code == 200:
            print('SUCCESS: Posted device list to Splunk HTTP event collector.')
        else:
            print(f'ERROR: Failed to post to Splunk HTTP event collector: http response code {response.status_code}')
    else:
        print('STATUS: No devices to send to Splunk.')
    print('STATUS: Finished execution.')

