const { GLib, Gdk, Gtk } = imports.gi;
import * as Utils from 'resource:///com/github/Aylur/ags/utils.js'

const range = (length, start = 1) => Array.from({ length }, (_, i) => i + start);

////////////////////// window manager specific method //////////////////////
export function GdkMonitorFromName(name) {
    const monitors = JSON.parse(Utils.exec('hyprctl -j monitors')); // change this command for a different window manager
    const monitor = monitors.find(monitor => monitor.name === name);
    // get all available gdk monitor objects for i in range of number of monitors
    const gdkmonitors = range(Gdk.Display.get_default()?.get_n_monitors() || 1, 0).map(i => Gdk.Display.get_default()?.get_monitor(i));
    // find the gdk monitor object that matches the monitor name
    const gdkmonitor = gdkmonitors.find(gdkmonitor => gdkmonitor?.get_model() === monitor.model);
    return gdkmonitor;
}
////////////////////////////////////////////////////////////////////////////
globalThis.GdkMonitorFromName = GdkMonitorFromName;