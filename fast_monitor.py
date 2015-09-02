# This class is dumped-down version of datadogpy which only query the monitor
# endpoint

import json
import urllib
import urllib2

class FastMonitor():
    def __init__(self, api_key=None, app_key=None, api_host=None):
        self.api_key = api_key
        self.app_key = app_key
        if api_host:
            self.api_host = api_host
        else:
            self.api_host = "https://app.datadoghq.com"

    def query_all(self):
        "Return a list of all monitor objects"
        url = self.api_host + "/api/v1/monitor"
        url += "?api_key={0}&application_key={1}".format(self.api_key, self.app_key)
        rep = urllib2.urlopen(url)
        return json.loads(rep.read())

if __name__ == "__main__":
    with open("datadog.conf", "r") as f:
        creds = f.read()

    creds = json.loads(creds)
    f = FastMonitor(**creds)
    monitors = f.query_all()
    for monitor in monitors:
        print monitor["id"], monitor["name"]
