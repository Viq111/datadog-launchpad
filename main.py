import json
import time

from launchpad_interface import MainController, ModeController
from ops_mode import OpsMode

if __name__ == "__main__":
    import launchpad2 as launchpad
    l = launchpad.Launchpad()
    controller = MainController(l)

    datadog_ops = OpsMode("datadog.conf")
    # Load ops.conf
    with open("ops.conf", "r") as f:
        monit = json.loads(f.read())
    for category, monitors in monit:
        for m in monitors:
            datadog_ops.add_monitor(m, category)

    controller.add_mode(datadog_ops)

    controller.start()
    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        controller.stop()
    print "Quiting... please wait"
    controller.join()
    l.all_off()
