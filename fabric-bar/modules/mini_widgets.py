import psutil
import os
from fabric.widgets.box import Box
from fabric.widgets.widget import Widget
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.eventbox import EventBox
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.scale import Scale
from fabric.widgets.button import Button
# from fabric.system_tray.widgets import SystemTray
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.utils import (
    FormattedString,
    bulk_replace,
    invoke_repeater,
    get_relative_path,
)
from fabric.core.service import Property
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from utils.icon_utils import icon_image_from_name, update_image_from_name


class VolumeWidget(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            from fabric.audio.service import Audio
        except Exception as e:
            print(e)
        self.audio = Audio()
        self._volume = 0

        self.vol_label = Label(label="0%", style="margin: 0px 6px 0px 0px; font-size: 18px")
        self.progress_bar = CircularProgressBar(
            name="volume-progress-bar", pie=True, size=24
        )
        self.vol_icon = icon_image_from_name("audio-volume-high-symbolic", 24)
        self.vol_level_desc = "high"

        self.event_box = EventBox(
            events="scroll",
            child=Box(spacing=4, children=[self.vol_icon, self.vol_label]),
        )

        self.audio.connect("notify::speaker", self.on_speaker_changed)
        self.event_box.connect("scroll-event", self.on_scroll)
        self.event_box.connect("button-press-event", self.on_clicked)
        self.add(self.event_box)

    @Property(float, "read-write", default_value=0.0)
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        return

    def on_clicked(self, _, event):
        if event.button == 1:
            self.audio.speaker.muted = not self.audio.speaker.muted
            self.set_volume_icon()
        elif event.button == 3:
            # open pavucontrol
            os.system("pavucontrol")
        return

    def on_scroll(self, _, event):
        match event.direction:
            case 0:
                self.audio.speaker.volume += 8
            case 1:
                self.audio.speaker.volume -= 8
        return
    
    def set_volume_icon(self):
        if self.audio.speaker.volume == 0 or self.audio.speaker.muted:
            update_image_from_name(self.vol_icon, "audio-volume-muted-symbolic")
            self.vol_level_desc = "muted"
        elif self.audio.speaker.volume < 34:
            update_image_from_name(self.vol_icon, "audio-volume-low-symbolic")
            self.vol_level_desc = "low"
        elif self.audio.speaker.volume < 67:
            update_image_from_name(self.vol_icon, "audio-volume-medium-symbolic")
            self.vol_level_desc = "medium"
        else:
            update_image_from_name(self.vol_icon, "audio-volume-high-symbolic")
            self.vol_level_desc = "high"

    def update_vol(self, v):
        self.volume = v
        self.set_volume_icon()
        self.vol_label.set_text(f"{round(v)} %")

    def on_speaker_changed(self, *_):
        if not self.audio.speaker:
            return
        
        self.volume = self.audio.speaker.volume
        self.update_vol(self.volume)

        self.set_tooltip_text(f"Volume: {round(self.volume)} %")

        self.audio.speaker.bind(
            "volume", "volume", self, lambda _, v: self.update_vol(v)
        )
        return
    
    def update(self):
        return True


class RAMWidget(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progress_bar = Gtk.ProgressBar(
            name ="ram-progress-bar",
            orientation=Gtk.Orientation.HORIZONTAL,
            fraction=0,
            show_text=False,
            text="RAM",
            **kwargs
            )
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_spacing(4)
        self.add(icon_image_from_name("memory-symbolic", 16))
        self.add(self.progress_bar)

        self.progress_bar.set_margin_bottom(10)
    
    def get(self):
        return self

    def update(self):
        # self.ram_progress_bar.value = psutil.virtual_memory().percent / 100
        self.progress_bar.set_fraction((psutil.virtual_memory().percent)/100) 
        self.set_tooltip_text(f"RAM Percent: {psutil.virtual_memory().percent}%")
        return True

class CPUWidget(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.progress_bar = Gtk.ProgressBar(
            name ="cpu-progress-bar",
            # fraction=0.01,
            show_text=False,
            text="CPU",
            **kwargs
            )
        self.set_spacing(4)

        self.add(icon_image_from_name("cpu-symbolic", 16))
        self.add(self.progress_bar)

        self.progress_bar.set_margin_bottom(10)

    def get(self):
        return self

    def update(self):
        cpu_percent = psutil.cpu_percent() # interval of 1 sec
        self.progress_bar.props.fraction = cpu_percent/100
        self.set_tooltip_text(f"CPU Percent: {round(cpu_percent)}%")
        return True


class BatteryWidget(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.battery_icon = icon_image_from_name("battery-full-symbolic", 16)
        self.battery_label = Label(label="100 %", style="margin: 0px 6px 0px 0px; font-size: 18px")
        
        self.pack_start(self.battery_icon, True, True, 4)
        self.pack_start(self.battery_label, True, True, 0)

    def set_battery_icon_from_percentage(self, bat_percent, charging=False):
        bar_percent_10 = bat_percent//10
        if bar_percent_10 < 10:
            bar_percent_10 += 1
        icon_name = "battery-" + ("0" if bar_percent_10<10 else "") + str(bar_percent_10*10)
        if charging:
            icon_name += "-charging"
        pixbuf = Gtk.IconTheme.get_default().load_icon(icon_name, 16, 0)
        self.battery_icon.set_from_pixbuf(pixbuf)

    def get(self):
        return self

    def update(self):
        if not (bat_sen := psutil.sensors_battery()):
            self.battery_icon.set_from_icon_name("battery-missing-symbolic")
            self.battery_label.set_text("N/A")
            self.set_tooltip_text("Battery: N/A")
        else:
            self.set_battery_icon_from_percentage(round(bat_sen.percent), bat_sen.power_plugged)
            # show battery state as well as percent in the tooltip
            self.set_tooltip_text(f"Battery" + (" charging " if bat_sen.power_plugged else "") + f": {round(bat_sen.percent)}%")
            self.battery_label.set_text(f"{round(bat_sen.percent)} %")
        return True