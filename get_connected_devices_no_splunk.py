# requests==2.25.1
import requests
from requests.auth import HTTPBasicAuth
# urllib3==1.26.3
import urllib3
import json


def get_connected_devices(url, admin, passwd):
    r = requests.get(url, auth=HTTPBasicAuth(admin, passwd), verify=False)
    devices = r.text.splitlines()[1][7:]
    return r.status_code, devices


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
    print('STATUS: Finished execution.')

