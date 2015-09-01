# Launchpad interface is the main interface to your launchpad
# You must (optionally derivate) and instance a ModeController interface
# You can then derivate from a ButtonView:
# - press() is called eah time the user press the button
# - get_status() is called at each refresh and returns a status which will be
#   translated by the controller to a LightMode and a color

import threading
import time

from launchpad2 import LightColor, LightMode

class _InputHandler(threading.Thread):
    "Fast handler for buttons inputs"
    def __init__(self, master, l):
        self.master = master
        self.l = l
        self.running = False

        threading.Thread.__init__(self)

    def run(self):
        self.running = True
        while self.running:
            inputs = self.l.get_all_inputs()
            if inputs:
                self.master.notify(inputs)
            time.sleep(0.01)

    def stop(self):
        self.running = False

class MainController(threading.Thread):
    def __init__(self, l, refresh=10):
        "Create a controller for the launchpad instance"
        self.l = l
        self.refresh = refresh
        self.running = False
        self.modes = []
        self.current_mode = 0 # Up to 7 different modes availables
        self.i_handler = _InputHandler(self, l)

        threading.Thread.__init__(self)

    def _mode_to_button(self, mode):
        return (8-mode) * 10 + 9
    def _button_to_mode(self, button):
        return 8 - (button-9) / 10

    def _refresh_mode_buttons(self):
        "Init mode color"
        self.l.all_off() # Reset all LEDs
        for i in range(8):
            button = self._mode_to_button(i)
            if i < len(self.modes):
                if i == self.current_mode:
                    self.l.led_on(button, LightColor.GREEN)
                else:
                    self.l.led_on(button, LightColor.DARK_BLUE)
            else:
                self.l.led_off(button)

    def add_mode(self, mode):
        "Add a mode controller"
        if not isinstance(mode, ModeController):
            raise RuntimeError("Mode must be of type ModeController")
        if len(self.modes) >= 8:
            print "ERROR: You have already 8 modes, can't add more"
        self.modes.append(mode)

    def notify(self, inputs):
        "Notified when the user click a button"
        mode = self.modes[self.current_mode]
        mode_buttons = [self._mode_to_button(i) for i in range(len(self.modes))]
        # Process actions
        for input_ in inputs:
            if input_ not in mode_buttons:
                mode.notify_action(input_)

        # Process mode change if there is one
        for input_ in inputs:
            if input_ in mode_buttons:
                self.current_mode = self._button_to_mode(input_)
                self._refresh_mode_buttons()

    def run(self):
        self.running = True
        self.i_handler.start()
        self._refresh_mode_buttons()

        while self.running:
            mode = self.modes[self.current_mode]
            # Update status
            for button, (color, light_mode) in mode.get_status():
                self.l.led_on(button, color, light_mode)
            time.sleep(self.refresh)

        self.i_handler.join()

    def stop(self):
        "Tell the controller to stop running"
        self.running = False
        self.i_handler.stop()

class ModeController():
    """Define a mode for the launchpad
    Must implement:
    - notify_action(button) which take a button position and do an action
    -  get_status() which returns a dict button <-> (light_color, light_mode)
    """
    def __init__(self):
        pass

    def notify_action(self, button):
        print "Unassigned action to button", button

    def get_status(self):
        return {}


if __name__ == "__main__":
    import launchpad2 as launchpad
    # Test with 4 modes
    l = launchpad.Launchpad()
    controller = MainController(l, 0.1)
    for i in range(4):
        mode = ModeController()
        controller.add_mode(mode)
    controller.start()
    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        controller.stop()
    print "Quiting... please wait"
    controller.join()
    l.all_off()
