const { GLib, Gdk, Gtk } = imports.gi;
import * as Utils from 'resource:///com/github/Aylur/ags/utils.js'

////////////////////// window manager specific method //////////////////////
export function GdkMonitorFromName(name) {
    const monitors = JSON.parse(Utils.exec('hyprctl -j monitors')); // change this command for a different window manager
    const monitor = monitors.find(monitor => monitor.name === name);
    const gdkmonitor = Gdk.Display.get_default()?.get_monitor_at_point(monitor.x, monitor.y) || 1;
    return gdkmonitor;
}
////////////////////////////////////////////////////////////////////////////
globalThis.GdkMonitorFromName = GdkMonitorFromName;