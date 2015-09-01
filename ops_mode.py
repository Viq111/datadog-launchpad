import json
import time
import webbrowser

from datadog import initialize, api
from launchpad2 import LightColor, LightMode
from launchpad_interface import ModeController

# The OpsMode is specially designed to associate a button on the launchpad
# to a datadog monitor
# Each line on the launchpad is associated to a category
# which we usually describe as a service
# You can also use only 1, 2, 4 columns per category
# categories will be assigned by order of addition

STATUS_TO_LIGHT = {
    "ok": (LightColor.GREEN, LightMode.ON),
    "alert": (LightColor.RED, LightMode.PULSE),
    "warn": (LightColor.ORANGE, LightMode.ON),
    "no data": (LightColor.GREY, LightMode.ON)
}

class OpsMode(ModeController):
    def __init__(self, colunms_per_category=8):
        "Set up a ops mode to datadog"
        if colunms_per_category not in [1 ,2, 4, 8]:
            raise RuntimeError("colunms_per_category must be 1, 2, 4 or 8")
        self.col = colunms_per_category
        self.categories = [] # List of [category, nb_monitors]
        self.button_id = {} # Assign a button <-> monitor_id

        # Initialize datadog
        with open("datadog.conf", "r") as f:
            conf = json.loads(f.read())
        initialize(api_key=conf['api_key'], app_key=conf['app_key'])

        ModeController.__init__(self)

    def _max_nb_categories(self):
        return 64 / self.col

    def _button_to_launchpad_button(self, button):
        """
        The launchpad bottom left button is 11, going one column on the left is
        + 1 and going one row up is +10
        In our design, we use 0 on top left, 7 on top right and 63 on bottom right
        """
        row = button / 8
        col = button % 8
        return (8 - row) * 10 + col + 1

    def _assign_button(self, category):
        "Return the num of the button"
        # Add the category if it doesn't exist
        if category not in [c[0] for c in self.categories]:
            self.categories.append([category, 1])
            if len(self.categories) > self._max_nb_categories():
                raise RuntimeError("You already used the maximum number of categories")
            row = len(self.categories) - 1
            col = 0
        else: # Add it to the category
            for i, c in enumerate(self.categories):
                if category == c[0]:
                    c[1] += 1
                    if c[1] > self.col:
                        raise RuntimeError("You already used the maximum number of monitor in {}".format(category))
                    row = i
                    col = c[1] - 1
                    break
        return self._button_to_launchpad_button(row * 8 + col)

    def _status_to_light(self, status):
        "Return a LightColor and LightMode"
        status = status.lower()
        if status in STATUS_TO_LIGHT:
            return STATUS_TO_LIGHT[status]
        else:
            return (LightColor.GREY, LightMode.BLINK)

    def add_monitor(self, id, category):
        "Assign a new monitor by its id to a category"
        button = self._assign_button(category)
        self.button_id[button] = id

    def notify_action(self, button):
        "Notified when you click on a button"
        id_ = self.button_id.get(button)
        if id_ is None:
            print "No monitor assigned to this button"
        else:
            url = "https://app.datadoghq.com/monitors#{}".format(id_)
            webbrowser.open(url)

    def get_status(self):
        "Get monitor status"
        result = []
        print "Querying datadog..."
        for button, monitor_id in self.button_id.iteritems():
            status = api.Monitor.get(monitor_id)
            col_mode = self._status_to_light(status.get('overall_state'))
            result.append((button, col_mode))
        print "Finished querying datadog"
        return result
