"use strict";
// Import
import Gdk from 'gi://Gdk';
import GLib from 'gi://GLib';
import App from 'resource:///com/github/Aylur/ags/app.js'
import * as Utils from 'resource:///com/github/Aylur/ags/utils.js'
// Stuff
import userOptions from './modules/.configuration/user_options.js';
import { firstRunWelcome } from './services/messages.js';
// Widgets
import { Bar, BarCornerTopleft, BarCornerTopright } from './modules/bar/main.js';
import Cheatsheet from './modules/cheatsheet/main.js';
import DesktopBackground from './modules/desktopbackground/main.js';
import Dock from './modules/dock/main.js';
import Corner from './modules/screencorners/main.js';
import Indicator from './modules/indicators/main.js';
import Osk from './modules/onscreenkeyboard/main.js';

import Overview from './modules/overview/main_overview.js';
import Applauncher from './modules/overview/main_search.js';

import Session from './modules/session/main.js';
import SideLeft from './modules/sideleft/main.js';
import SideRight from './modules/sideright/main.js';
import Click2Close from './modules/click2close/main.js';

const COMPILED_STYLE_DIR = `${GLib.get_user_cache_dir()}/ags/user/generated`

function forMonitors(widget) {
    const monitors = JSON.parse(Utils.exec('hyprctl monitors -j'));
    for (const monitor of monitors) {
        widget(monitor.name);//.catch(print);
    }
}

// SCSS compilation
Utils.exec(`bash -c 'echo "" > ${App.configDir}/scss/_musicwal.scss'`); // reset music styles
Utils.exec(`bash -c 'echo "" > ${App.configDir}/scss/_musicmaterial.scss'`); // reset music styles
async function applyStyle() {
    Utils.exec(`mkdir -p ${COMPILED_STYLE_DIR}`);
    Utils.exec(`sass ${App.configDir}/scss/main.scss ${COMPILED_STYLE_DIR}/style.css`);
    App.resetCss();
    App.applyCss(`${COMPILED_STYLE_DIR}/style.css`);
    console.log('[LOG] Styles loaded')
}
applyStyle().catch(print);
globalThis.mybar = Bar;
globalThis.appl = Applauncher;
globalThis.mymonitors = JSON.parse(Utils.exec('hyprctl monitors -j'));
const Windows = () => [
    // forMonitors(DesktopBackground),
    Overview(),
    Applauncher(),
    forMonitors(Indicator),
    forMonitors(Cheatsheet),
    SideLeft(),
    SideRight(),
    forMonitors(Osk),
    Session(),
    userOptions.dock.enabled ? forMonitors(Dock) : null,
    ...(userOptions.appearance.fakeScreenRounding ? [
        forMonitors((monitor_name) => Corner(monitor_name, 'top left', true)),
        forMonitors((monitor_name) => Corner(monitor_name, 'top right', true)),
    ] : []),
    forMonitors((monitor_name) => Corner(monitor_name, 'bottom left', userOptions.appearance.fakeScreenRounding)),
    forMonitors((monitor_name) => Corner(monitor_name, 'bottom right', userOptions.appearance.fakeScreenRounding)),
    forMonitors(BarCornerTopleft),
    forMonitors(BarCornerTopright),
    forMonitors(Click2Close),
];

const CLOSE_ANIM_TIME = 210; // Longer than actual anim time to make sure widgets animate fully
const closeWindowDelays = {}; // For animations
for (let i = 0; i < (Gdk.Display.get_default()?.get_n_monitors() || 1); i++) {
    closeWindowDelays[`osk${i}`] = CLOSE_ANIM_TIME;
}

App.config({
    css: `${COMPILED_STYLE_DIR}/style.css`,
    stackTraceOnError: true,
    closeWindowDelay: closeWindowDelays,
    windows: Windows().flat(1),
});

// launching the bars 
// works only for one monitor
forMonitors(Bar);