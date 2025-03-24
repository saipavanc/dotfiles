import gi
import re
import json
import os, subprocess
from loguru import logger
from fabric.core.service import Property
from collections.abc import Iterable, Callable
from typing import Literal
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.hyprland.service import Hyprland, HyprlandEvent
from fabric.utils.helpers import FormattedString, bulk_connect, truncate, exec_shell_command_async

from utils.icon_utils import icon_image_from_name, update_image_from_name

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

def add_hover_cursor(widget):
    # Add enter/leave events to change the cursor
    widget.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
    widget.connect("enter-notify-event", lambda w, e: w.get_window().set_cursor(Gdk.Cursor.new_from_name(w.get_display(), "pointer")) if w.get_window() else None)
    widget.connect("leave-notify-event", lambda w, e: w.get_window().set_cursor(None) if w.get_window() else None)

######### Methods to communicate with Hyprland #########

connection: Hyprland | None = None

def get_hyprland_connection() -> Hyprland:
    global connection
    if not connection:
        connection = Hyprland()

    return connection

def hyprland_monitor_info(monitor_name:str):
    monitors = json.loads(
        str(get_hyprland_connection().send_command("j/monitors").reply.decode())
    )
    for monior in monitors:
        if monior["name"]==monitor_name:
            return monior
    raise ValueError(f"Monitor {monitor_name} not found")

def active_workspace_id_on_monitor(monitor_name:str):
    monitor = hyprland_monitor_info(monitor_name)
    return monitor['activeWorkspace']['id']

def get_all_workspaces():
    workspaces=json.loads(
        str(get_hyprland_connection().send_command("j/workspaces").reply.decode())
    )
    return workspaces

def workspace_ids_on_monitor(monitor_name:str):
    workspaces=json.loads(
        str(get_hyprland_connection().send_command("j/workspaces").reply.decode())
    )
    return [workspace["id"] for workspace in workspaces if workspace["monitor"]==monitor_name]

def active_client_on_monitor(monitor_name:str):
    active_workspace_id = active_workspace_id_on_monitor(monitor_name)
    workspaces=json.loads(
        str(get_hyprland_connection().send_command("j/workspaces").reply.decode())
    )
    active_workspace_on_monitor = [workspace for workspace in workspaces if workspace["id"]==active_workspace_id][0]
    clients=json.loads(
        str(get_hyprland_connection().send_command("j/clients").reply.decode())
    )
    active_client = [client for client in clients if client["address"]==active_workspace_on_monitor["lastwindow"]]
    if len(active_client)==0:
        return {}
    return active_client[0]

def active_client_title_on_monitor(monitor_name:str):
    active_client = active_client_on_monitor(monitor_name)
    return active_client.get("class", ""), active_client.get("title", "")

def workspace_id_of_window(window_id:str):
    clients=json.loads(
        str(get_hyprland_connection().send_command("j/clients").reply.decode())
    )
    client = [client for client in clients if client["address"]==window_id]
    if len(client)==0:
        return -1
    return client[0]["workspace"]["id"]

def is_workspace_occuppied(workspace_id:int):
    clients=json.loads(
        str(get_hyprland_connection().send_command("j/clients").reply.decode())
    )
    return any([client["workspace"]["id"]==workspace_id for client in clients])

###################################################################

class WorkspaceButton(Button):
    @Property(int, "readable")
    def id(self) -> int:
        return self._id

    @Property(bool, "read-write", default_value=False)
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool):
        self._active = value
        if value is True:
            self.urgent = False
        (self.remove_style_class if not value else self.add_style_class)("active")
        return self.do_bake_label()

    @Property(bool, "read-write", default_value=False)
    def urgent(self) -> bool:
        return self._urgent

    @urgent.setter
    def urgent(self, value: bool):
        self._urgent = value
        (self.remove_style_class if not value else self.add_style_class)("urgent")
        return self.do_bake_label()

    @Property(bool, "read-write", default_value=True)
    def empty(self) -> bool:
        return self._empty

    @empty.setter
    def empty(self, value: bool):
        self._empty = value
        (self.remove_style_class if not value else self.add_style_class)("empty")
        return self.do_bake_label()

    def __init__(
        self,
        id: int,
        label: FormattedString | str | None = None,
        image: Gtk.Image | None = None,
        child: Gtk.Widget | None = None,
        name: str | None = None,
        visible: bool = True,
        all_visible: bool = False,
        style: str | None = None,
        style_classes: Iterable[str] | str | None = None,
        tooltip_text: str | None = None,
        tooltip_markup: str | None = None,
        h_align: Literal["fill", "start", "end", "center", "baseline"]
        | Gtk.Align
        | None = None,
        v_align: Literal["fill", "start", "end", "center", "baseline"]
        | Gtk.Align
        | None = None,
        h_expand: bool = False,
        v_expand: bool = False,
        size: Iterable[int] | int | None = None,
        **kwargs,
    ):
        super().__init__(
            None,
            image,
            child,
            name,
            visible,
            all_visible,
            style,
            style_classes,
            tooltip_text,
            tooltip_markup,
            h_align,
            v_align,
            h_expand,
            v_expand,
            size,
            **kwargs,
        )
        self._id: int = id
        self._label: FormattedString | None = (
            FormattedString(label) if isinstance(label, str) else label
        )
        self._active: bool = False
        self._urgent: bool = False
        self._empty: bool = True

        self.active = False
        self.urgent = False
        self.empty = True

    def do_bake_label(self):
        if not self._label:
            return
        return self.set_label(self._label.format(button=self))


class Workspaces(EventBox):
    @staticmethod
    def default_buttons_factory(workspace_id: int):
        return WorkspaceButton(id=workspace_id, label=str(workspace_id))

    def __init__(
        self,
        monitor_name: str,
        buttons: Iterable[WorkspaceButton] | None = None,
        buttons_factory: Callable[[int], WorkspaceButton | None]
        | None = default_buttons_factory,
        invert_scroll: bool = False,
        empty_scroll: bool = False,
        **kwargs,
    ):
        super().__init__(events="scroll")
        self.connection = get_hyprland_connection()
        self._container = Box(**kwargs)
        self.children = self._container
        self.monitor_name:str = monitor_name

        self._active_workspace: int | None = None
        self._buttons: dict[int, WorkspaceButton] = {}
        self._buttons_preset: list[WorkspaceButton] = [
            button for button in buttons or ()
        ]
        self._buttons_factory = buttons_factory
        self._invert_scroll = invert_scroll
        self._empty_scroll = empty_scroll

        bulk_connect(
            self.connection,
            {
                "event::workspace": self.on_workspace,
                "event::createworkspace": self.on_createworkspace,
                "event::destroyworkspace": self.on_destroyworkspace,
                "event::urgent": self.on_urgent,
                "event::openwindow": self.on_window_open,
                "event::closewindow": self.on_window_close,
                "event::movewindow": self.on_window_close,
                "event::moveworkspacev2":self.on_move_workspace,
            },
        )

        # all aboard...
        if self.connection.ready:
            self.on_ready(None)
        else:
            self.connection.connect("event::ready", self.on_ready)
        self.connect("scroll-event", self.scroll_handler)

    def on_move_workspace(self, _, event: HyprlandEvent):
        if len(event.data) < 1:
            return
        WORKSPACEID,WORKSPACENAME,MONNAME = event.data
        # if WORKAPACEID in workspaces then remove it
        if WORKSPACEID in self._buttons:
            self.remove_button(self._buttons[WORKSPACEID])
            self.open_workspaces.remove(WORKSPACEID)

        if MONNAME != self.monitor_name:
            return
        # if reached here then add the workspace
        self.open_workspaces.append(WORKSPACEID)
        if not (btn := self.lookup_or_bake_button(WORKSPACEID)):
            return
        btn.empty = not is_workspace_occuppied(WORKSPACEID)
        return self.insert_button(btn)
    

    def on_ready(self, _):
        open_workspaces: tuple[int, ...] = workspace_ids_on_monitor(self.monitor_name)
        self.open_workspaces = open_workspaces
        self._active_workspace = active_workspace_id_on_monitor(self.monitor_name)
        for btn in self._buttons_preset:
            self.insert_button(btn)

        for id in open_workspaces:
            if not (btn := self.lookup_or_bake_button(id)):
                continue

            if id == self._active_workspace:
                btn.active = True
            btn.empty = not is_workspace_occuppied(id)

            if btn in self._buttons_preset:
                continue

            self.insert_button(btn)
        return
    
    def on_window_open(self, _, event: HyprlandEvent):
        if len(event.data) < 1:
            return
        opened_workspace = int(event.data[1])
        if opened_workspace not in self.open_workspaces:
            return
        if not (btn := self._buttons.get(opened_workspace)):
            return
        btn.empty = False
    
    def on_window_close(self, _, event: HyprlandEvent):
        if len(event.data) < 1:
            return
        for btn in self._buttons.values():
            btn.empty = not is_workspace_occuppied(btn.id)

    def on_workspace(self, _, event: HyprlandEvent):
        if len(event.data) < 1:
            return

        active_workspace = self.do_get_workspace_id(event)
        if active_workspace not in self.open_workspaces:
            return
        if active_workspace == self._active_workspace:
            return

        if self._active_workspace is not None and (
            old_btn := self._buttons.get(self._active_workspace)
        ):
            old_btn.active = False

        self._active_workspace = active_workspace
        if not (btn := self.lookup_or_bake_button(active_workspace)):
            return

        btn.urgent = False
        btn.active = True

        if btn in self._container.children:
            return
        return self.insert_button(btn)

    def on_createworkspace(self, _, event: HyprlandEvent):
        if len(event.data) < 1:
            return
        new_workspace = self.do_get_workspace_id(event)
        if not new_workspace in workspace_ids_on_monitor(self.monitor_name):
            return
        self.open_workspaces.append(new_workspace)

        if not (btn := self.lookup_or_bake_button(new_workspace)):
            return

        btn.empty = False
        if btn in self._buttons_preset:
            return
        return self.insert_button(btn)

    def on_destroyworkspace(self, _, event: HyprlandEvent):
        if len(event.data) < 1:
            return

        destroyed_workspace = self.do_get_workspace_id(event)
        if destroyed_workspace not in self.open_workspaces:
            return
        self.open_workspaces.remove(destroyed_workspace)
        if not (btn := self._buttons.get(destroyed_workspace)):
            return  # doens't exist, skip

        btn.active = False
        btn.urgent = False
        btn.empty = True

        if btn in self._buttons_preset:
            return
        return self.remove_button(btn)

    def on_urgent(self, _, event: HyprlandEvent):
        if len(event.data) < 1:
            return

        clients = json.loads(self.connection.send_command("j/clients").reply.decode())
        clients_map = {client["address"]: client for client in clients}
        urgent_client: dict = clients_map.get("0x" + event.data[0], {})
        if not (raw_workspace := urgent_client.get("workspace")):
            return logger.warning(
                f"[Workspaces] received urgent signal, but data received ({event.data[0]}) is uncorrect, skipping..."
            )

        urgent_workspace = int(raw_workspace["id"])
        if not (btn := self._buttons.get(urgent_workspace)):
            return  # doens't exist, skip

        btn.urgent = True
        return logger.info(f"[Workspaces] workspace {urgent_workspace} is now urgent")

    def scroll_handler(self, _, event: Gdk.EventScroll):
        cmd = "" if self._empty_scroll else "e"
        match event.direction:  # type: ignore
            case Gdk.ScrollDirection.UP:
                cmd += "-1" if self._invert_scroll is True else "+1"
                logger.info("[Workspaces] Moving to the next workspace")
            case Gdk.ScrollDirection.DOWN:
                cmd += "+1" if self._invert_scroll is True else "-1"
                logger.info("[Workspaces] Moving to the previous workspace")
            case _:
                return logger.warning(
                    f"[Workspaces] Unknown scroll direction ({event.direction})"  # type: ignore
                )
        return self.connection.send_command(f"batch/dispatch workspace {cmd}")

    def insert_button(self, button: WorkspaceButton) -> None:
        self._buttons[button.id] = button
        self._container.add(button)
        button.connect("clicked", self.do_handle_button_press)
        return self.reorder_buttons()

    def reorder_buttons(self):
        for _, child in sorted(self._buttons.items(), key=lambda i: i[0]):
            self._container.reorder_child(child, (child.id - 1))
        return

    def remove_button(self, button: WorkspaceButton) -> None:
        if self._buttons.pop(button.id, None) is not None:
            self._container.remove(button)
        return button.destroy()

    def lookup_or_bake_button(self, workspace_id: int) -> WorkspaceButton | None:
        if not (btn := self._buttons.get(workspace_id)):
            if self._buttons_factory:
                btn = self._buttons_factory(workspace_id)
        return btn

    def do_handle_button_press(self, button: WorkspaceButton):
        self.connection.send_command(f"batch/dispatch workspace {button.id}")
        return logger.info(f"[Workspaces] Moved to workspace {button.id}")

    def do_get_workspace_id(self, event: HyprlandEvent) -> int:
        if "special" in (ws := event.data[0]):
            return -99
        return int(ws)


class ActiveWindow(Button):
    def __init__(
        self,
        monitor_name: str,
        formatter: FormattedString = FormattedString(
            "{'' if not win_title else truncate(win_title, 42)}",
            truncate=truncate,
        ),
        # TODO: hint super's kwargs
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.connection = get_hyprland_connection()
        self.formatter = formatter
        self.monitor_name:str = monitor_name
        self.workspace_id_list = [ws["id"] for ws in get_all_workspaces()]
        self.active_window_label = Label(label="", style="margin: 0px 6px 4px 4px; font-size: 18px")
        self.active_window_icon = Gtk.Image.new_from_icon_name("window", 20)

        self.box = Box(spacing=4, children=[self.active_window_icon, self.active_window_label])
        self.add(self.box)

        bulk_connect(
            self.connection,
            {
                "event::activewindow": self.on_activewindow,
                "event::closewindow": self.on_closewindow,
            },
        )

        # connect right click to open context menu
        self._build_context_menu()
        self.connect("button-press-event", self.on_button_press_event)

        # all aboard...
        if self.connection.ready:
            self.on_ready(None)
        else:
            self.connection.connect("event::ready", self.on_ready)

    def on_button_press_event(self, _, event: Gdk.EventButton):
        if event.button != 3:
            return
        # make a context menu for this button
        print("Right clicked on the active window")
        self.cmenu.popup_at_pointer()
        # return logger.info("[ActiveWindow] Right clicked on the active window")
    
    def _build_context_menu(self):
        self.cmenu = Gtk.Menu.new()
        self.cm_item_list = [Gtk.MenuItem.new_with_label(f"Workspace {ws_id}") for ws_id in self.workspace_id_list]
        for menu_item in self.cm_item_list:
            menu_item.connect("activate", self.on_menu_item_activate)
            self.cmenu.append(menu_item)
        self.cmenu.show_all()

    def on_menu_item_activate(self, menu_item):
        ws_id = self.workspace_id_list[self.cm_item_list.index(menu_item)]
        self.connection.send_command(f"batch/dispatch movetoworkspace {ws_id}")
        return logger.info(f"[ActiveWindow] Moved to workspace {ws_id}")

    def on_ready(self, _):
        return self.do_initialize(), logger.info(
            "[ActiveWindow] Connected to the hyprland socket"
        )

    def on_closewindow(self, _, event: HyprlandEvent):
        if len(event.data) < 1:
            return
        return self.do_initialize(), logger.info(
            f"[ActiveWindow] Closed window 0x{event.data[0]}"
        )

    def on_activewindow(self, _, event: HyprlandEvent):
        if len(event.data) < 2:
            return
        win_class, win_title = self.do_initialize()
        logger.info(
            f"[ActiveWindow] Activated window {win_class}, {win_title}"
        )

    def do_initialize(self):
        win_class, win_title = active_client_title_on_monitor(self.monitor_name)
        self.active_window_label.set_label(self.formatter.format(win_class=win_class, win_title=win_title))
        update_image_from_name(self.active_window_icon, win_class if win_class is not '' else None, 20)
        return win_class, win_title


class Language(Button):
    def __init__(
        self,
        keyboard: str = ".*",
        formatter: FormattedString = FormattedString("{language}"),
        # TODO: hint super's kwargs
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.connection = get_hyprland_connection()
        self.keyboard = keyboard
        self.formatter = formatter

        self.connection.connect("event::activelayout", self.on_activelayout)

        # all aboard...
        if self.connection.ready:
            self.on_ready(None)
        else:
            self.connection.connect("event::ready", self.on_ready)

    def on_ready(self, _):
        return self.do_initialize(), logger.info(
            "[Language] Connected to the hyprland socket"
        )

    def on_activelayout(self, _, event: HyprlandEvent):
        if len(event.data) < 2:
            return logger.warning(
                f"[Language] got invalid event data from hyprland, raw data is\n{event.raw_data}"
            )
        keyboard, language = event.data
        matched: bool = False

        if re.match(self.keyboard, keyboard) and (matched := True):
            self.set_label(self.formatter.format(language=language))

        return logger.debug(
            f"[Language] Keyboard: {keyboard}, Language: {language}, Match: {matched}"
        )

    def do_initialize(self):
        devices: dict[str, list[dict[str, str]]] = json.loads(
            str(self.connection.send_command("j/devices").reply.decode())
        )
        if not devices or not (keyboards := devices.get("keyboards")):
            return logger.warning(
                f"[Language] cound't get devices from hyprctl, gotten data\n{devices}"
            )

        language: str | None = None
        for kb in keyboards:
            if (
                not (kb_name := kb.get("name"))
                or not re.match(self.keyboard, kb_name)
                or not (language := kb.get("active_keymap"))
            ):
                continue

            self.set_label(self.formatter.format(language=language))
            logger.debug(
                f"[Language] found language: {language} for keyboard {kb_name}"
            )
            break

        return (
            logger.info(
                f"[Language] Could not find language for keyboard: {self.keyboard}, gotten keyboards: {keyboards}"
            )
            if not language
            else logger.info(
                f"[Language] Set language: {language} for keyboard: {self.keyboard}"
            )
        )

class CaffeineButton(Button):
    def __init__(self):
        self.caffeine_icon = Gtk.Image.new_from_icon_name("face-tired", 18)
        self.caffeine_label = Label(
            name="caffeine-label",
            label="Caffeine",
            justification="left",
        )
        self.caffeine_label_box = Box(children=[self.caffeine_label, Box(h_expand=True)])
        self.caffeine_status = Label(
            name="caffeine-status",
            label="Enabled",
            justification="left",
        )
        self.caffeine_status_box = Box(children=[self.caffeine_status, Box(h_expand=True)])
        self.caffeine_text = Box(
            name="caffeine-text",
            orientation="v",
            h_align="start",
            v_align="center",
            children=[self.caffeine_label_box, self.caffeine_status_box],
        )
        self.caffeine_box = Box(
            h_align="start",
            v_align="center",
            spacing=10,
            children=[self.caffeine_icon, self.caffeine_text],
        )
        super().__init__(
            name="caffeine-button",
            h_expand=True,
            child=self.caffeine_box,
            on_clicked=self.toggle_wlinhibit,
        )
        add_hover_cursor(self)  # <-- Added hover

        self.widgets = [self, self.caffeine_label, self.caffeine_status]
        self.check_wlinhibit()

    def toggle_wlinhibit(self, *args):
        """
        Toggle the 'wlinhibit' process:
          - If running, kill it and mark as 'Disabled' (add 'disabled' class).
          - If not running, start it and mark as 'Enabled' (remove 'disabled' class).
        """
        try:
            subprocess.check_output(["pgrep", "wlinhibit"])
            exec_shell_command_async("pkill wlinhibit")
            self.update_button(status_enabled=False)
        except subprocess.CalledProcessError:
            exec_shell_command_async("wlinhibit")
            self.update_button(status_enabled=True)

    def update_button(self, status_enabled):
        if status_enabled:
            self.caffeine_status.set_label("Enabled")
            update_image_from_name(self.caffeine_icon, "face-glasses", 18)
            for i in self.widgets:
                i.remove_style_class("disabled")
        else:
            self.caffeine_status.set_label("Disabled")
            update_image_from_name(self.caffeine_icon, "face-tired", 18)
            for i in self.widgets:
                i.add_style_class("disabled")

    def check_wlinhibit(self, *args):
        try:
            subprocess.check_output(["pgrep", "wlinhibit"])
            self.update_button(status_enabled=True)
        except subprocess.CalledProcessError:
            self.update_button(status_enabled=False)