import Widget from 'resource:///com/github/Aylur/ags/widget.js';
import { SearchAndWindows } from "./windowcontent.js";
import PopupWindow from '../.widgethacks/popupwindow.js';
import { GdkMonitorFromName } from './../../workspace_specific_methods.js';

export default (monitor_name = '') => PopupWindow({
    name: `overview-${monitor_name}`,
    gdkmonitor: GdkMonitorFromName(monitor_name),
    // exclusivity: 'ignore',
    keymode: 'exclusive',
    visible: false,
    anchor: ['top', 'bottom'],
    layer: 'overlay',
    child: Widget.Box({
        vertical: true,
        children: [
            SearchAndWindows(true),
        ]
    }),
})
