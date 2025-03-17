import psutil
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.eventbox import EventBox
from fabric.widgets.centerbox import CenterBox
# from fabric.system_tray.widgets import SystemTray
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.utils import (
    FormattedString,
    bulk_replace,
    invoke_repeater,
    get_relative_path,
)

from hyprland.hyprland_monitors import get_gdk_monitor_id_from_name, get_hyprctl_monitor_id_from_name
from hyprland.widgets import Language, ActiveWindow, Workspaces
from .system_tray.widgets import SystemTray
from .datetime_widget import DateTime
from .mini_widgets import RAMWidget, CPUWidget, VolumeWidget, BatteryWidget
from .metrics import MetricsSmall
# from .base import ModuleBase

class StatusBar(Window):
    def __init__(
        self,
        monitor_name,
        id_str:str = None,
        show_system_tray: bool = False,
    ):
        super().__init__(
            name="bar",
            layer="top",
            anchor="left top right",
            margin="5px 10px 3px 10px",
            exclusivity="auto",
            visible=False,
            all_visible=False,
            monitor=get_gdk_monitor_id_from_name(monitor_name),
        )
        # set stylesheet path
        self.stylesheet_path = get_relative_path("./bar_style.css")
        self.show_system_tray = show_system_tray

        self.id_str = id_str or f"StatusBar-{monitor_name}"
        self.workspaces = Workspaces(
            name="workspaces",
            spacing=4,
            monitor_name=monitor_name,
            # buttons_factory=lambda ws_id: WorkspaceButton(id=ws_id, label=None),
        )
        self.active_window = ActiveWindow(name="hyprland-window", monitor_name=monitor_name)
        self.date_time = DateTime(name="date-time", formatters=("%A %b %d %I:%M %p"))

        if self.show_system_tray:
            self.system_tray = SystemTray(name="system-tray", icon_theme_name="Papirus-Dark", spacing=4)

        self.status_widgets = {}
        # self.status_widgets["cpu_widget"] = CPUWidget()
        # self.status_widgets["ram_widget"] = RAMWidget()
        self.status_widgets["metrics_small"] = MetricsSmall()
        self.status_widgets["battery_widget"] = BatteryWidget()
        self.status_widgets["volume_widget"] = VolumeWidget()


        
        status_container_children = [widget for widget in self.status_widgets.values()]

        self.status_container = Box(
            name="widgets-container",
            spacing=4,
            orientation="h",
            # children=self.progress_bars_overlay,
            children=status_container_children,
        )

        left_children = [self.workspaces, self.active_window]
        center_children = []
        right_children = [self.status_container, self.date_time]
        if self.show_system_tray:
            # add system tray as the second element from last
            right_children.insert(-1, self.system_tray)

        self.children = CenterBox(
            name="bar-inner",
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=left_children,
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=center_children,
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=right_children,
            ),
        )

        # update all widgets
        for widget in self.status_widgets.values():
            invoke_repeater(1000, widget.update)
        # invoke_repeater(1000*60, self.update_battery_info)

        self.show_all()


# if __name__ == "__main__":
# def launch(monitor_name: str):
#     bar = StatusBar(monitor_name=monitor_name)
#     app = Application("bar", bar)
#     app.set_stylesheet_from_file(get_relative_path("./style.css"))

#     app.run()
#     return app
