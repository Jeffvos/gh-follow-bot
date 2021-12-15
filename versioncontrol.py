import json
import requests

class checkVersion():
    def __init__(self):
        try: 
            with open('version.json') as current:
                self.version_info = json.load(current)
                self.releases_url = self.version_info['releases_url']
                self.current_version = self.version_info['version']
                
        except FileNotFoundError:
            print('ERROR: version.json not found')
            quit()

    def running_latest(self):
        r = requests.get(self.releases_url)
        versions = r.json()
        for version in versions:
            if version['tag_name'] > self.current_version:
                msg_current = f"You are currently running version {self.current_version}"
                msg_latest = f"\nPlease upgrade to version {version['tag_name']}"
                print(msg_current,msg_latest)
                return False
            else:
                print(f"running the latest version {self.current_version}")
                return True
