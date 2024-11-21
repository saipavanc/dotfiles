
const { Gdk, Gtk } = imports.gi;
import App from 'resource:///com/github/Aylur/ags/app.js'
import Variable from 'resource:///com/github/Aylur/ags/variable.js';
import Mpris from 'resource:///com/github/Aylur/ags/service/mpris.js';
import * as Utils from 'resource:///com/github/Aylur/ags/utils.js';
const { exec, execAsync } = Utils;

Gtk.IconTheme.get_default().append_search_path(`${App.configDir}/assets/icons`);

// Global vars for external control (through keybinds)
export const showMusicControls = Variable(false, {})
export const showColorScheme = Variable(false, {})
globalThis['openMusicControls'] = showMusicControls;
globalThis['openColorScheme'] = showColorScheme;
globalThis['mpris'] = Mpris;

// Screen size
export const SCREEN_WIDTH = Number(exec(`bash -c "hyprctl monitors -j | jq -r '.[] | select(.id == '$(hyprctl activeworkspace -j | jq '.monitorID')' )' | jq '.width'"`));
export const SCREEN_HEIGHT = Number(exec(`bash -c "hyprctl monitors -j | jq -r '.[] | select(.id == '$(hyprctl activeworkspace -j | jq '.monitorID')' )' | jq '.height'"`));

export const getMonitorProperty = (property) => {
    let height = Number(exec(`bash -c "hyprctl monitors -j | jq -r '.[] | select(.id == '$(hyprctl activeworkspace -j | jq '.monitorID')' )' | jq '.height'"`)); 
    let width = Number(exec(`bash -c "hyprctl monitors -j | jq -r '.[] | select(.id == '$(hyprctl activeworkspace -j | jq '.monitorID')' )' | jq '.width'"`)); 
    const transform = Number(exec(`bash -c "hyprctl monitors -j | jq -r '.[] | select(.id == '$(hyprctl activeworkspace -j | jq '.monitorID')' )' | jq '.transform'"`));
    const result = 0;
    switch (transform) {
        case 1: // 90 degrees
            [width, height] = [height, width]; // Swap width and height
            break;
        case 3: // 180 degrees
            [width, height] = [height, width]; // Swap width and height
            break;
        default:
            // For 0 (normal) transform, no adjustment needed
            break;
    }
    if (property === 'height') {
        return height;
    }
    if (property === 'width') {
        return width;
    }
}
globalThis.mon = getMonitorProperty;

// Mode switching
export const currentShellMode = Variable('normal', {}) // normal, focus
globalThis['currentMode'] = currentShellMode;
globalThis['cycleMode'] = () => {
    if (currentShellMode.value === 'normal') {
        currentShellMode.value = 'focus';
    } else {
        currentShellMode.value = 'normal';
    }
}

// // Window controls
const range = (length, start = 1) => Array.from({ length }, (_, i) => i + start);
globalThis['toggleWindowOnAllMonitors'] = (name) => {
    range(Gdk.Display.get_default()?.get_n_monitors() || 1, 0).forEach(id => {
        App.toggleWindow(`${name}${id}`);
    });
}
globalThis['closeWindowOnAllMonitors'] = (name) => {
    range(Gdk.Display.get_default()?.get_n_monitors() || 1, 0).forEach(id => {
        App.closeWindow(`${name}${id}`);
    });
}
globalThis['openWindowOnAllMonitors'] = (name) => {
    range(Gdk.Display.get_default()?.get_n_monitors() || 1, 0).forEach(id => {
        App.openWindow(`${name}${id}`);
    });
}

globalThis['closeEverything'] = () => {
    // const numMonitors = Gdk.Display.get_default()?.get_n_monitors() || 1;
    // for (let i = 0; i < numMonitors; i++) {
    //     App.closeWindow(`cheatsheet${i}`);
    // }
    App.closeWindow(`cheatsheet`);
    App.closeWindow(`session`);
    App.closeWindow(`click2close`);
    App.closeWindow('sideleft');
    App.closeWindow('sideright');
    App.closeWindow('overview');
    App.closeWindow('applauncher');
};
