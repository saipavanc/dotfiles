################# conventions for launching windows or objects #################
# Each module should have the following property defined along with the attribute _id_str:
# @property
# def id_str(self) -> str:
#     if self._id_str is None:
#         return f"StatusBar-{self.monitor_name}"
#     return self._id_str
# @id_str.setter
# def id_str(self, value: str):
#     self._id_str = value


from fabric import Application
from fabric.utils import monitor_file, get_relative_path
from fabric.utils.helpers import exec_shell_command_async
from loguru import logger
from modules.status_bar import StatusBar
from modules.notifications import NotificationModule 
from modules.side_panel.config import SidePanel
from fabric import Application, Fabricator
from hyprland.hyprland_monitors import get_all_monitors

# change to current working directory
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def toggle_widget(widget):
    if widget.is_visible():
        widget.hide()
    else:
        widget.show()

def initialize_widgets():
    # define all the windows
    bars = []
    # bars.append(StatusBar(monitor_name="HDMI-A-1"))
    for monitor in get_all_monitors().values():
        show_system_tray = monitor == "eDP-1" # only show system tray on the laptop monitor
        bars.append(StatusBar(monitor_name=monitor, show_system_tray=show_system_tray))
    
    side_panel = SidePanel(name="side-panel")
    side_panel.hide() # hide the panel initially
    
    # Notification module
    notifs = NotificationModule(id_str="Notifications")

    # connect side panel to date-time of bars
    for bar in bars:
        def do_handle_press(bar, _, event, *args):
            match event.button:
                case 1:  # left click
                    toggle_widget(side_panel)
                case 3:  # right click
                    bar.date_time.do_cycle_prev()
            return
        bar.date_time.disconnect(bar.date_time.connect_dict["button-press-event"])
        bar.date_time.connect("button-press-event", lambda *args: do_handle_press(bar, *args))
    
    ###### All windows ########
    # list of windows
    windows = bars + [notifs] + [side_panel]
    return windows

if __name__ == "__main__":
    ############# Create Fabric Application  #############
    # create the fabric application
    app = Application("bar", *initialize_widgets())

    ####### apply stylesheet to the application #######
    def apply_stylesheet(*_):
        print("Applying stylesheet")
        return app.set_stylesheet_from_file(
            "./style.css"
        )
    #### look for changes in the style sheet and apply them ####
    style_monitor = monitor_file(get_relative_path("./"))
    style_monitor.connect("changed", apply_stylesheet)
    apply_stylesheet() # initial styling
    app.run()
