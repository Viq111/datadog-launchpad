import datadog
import requests


class FastMonitor():
    "Query datadog API either directly via the API or via http"
    def __init__(self, api_key=None, app_key=None, api_host=None, datadog_lib=True):
        self.api_key = api_key
        self.app_key = app_key
        self.dd = datadog_lib
        if api_host:
            self.api_host = api_host
        else:
            self.api_host = "https://app.datadoghq.com"
        if self.dd:
            datadog.initialize(api_host=api_host, api_key=api_key, app_key=app_key)

    def query_all(self):
        "Return a list of all monitor objects"
        if self.dd:
            return datadog.api.Monitor.get_all()
        else:
            url = self.api_host + "/api/v1/monitor"
            print "Querying {} ...".format(url)
            payload = {"api_key": self.api_key, "application_key": self.app_key}
            r = requests.get(url, params=payload)
            return r.json()

if __name__ == "__main__":
    import json

    with open("datadog.conf", "r") as f:
        creds = f.read()

    creds = json.loads(creds)
    f = FastMonitor(**creds)
    monitors = f.query_all()
    for monitor in monitors:
        print monitor["id"], monitor["name"]
