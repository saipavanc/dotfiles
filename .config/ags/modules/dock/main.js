import Widget from 'resource:///com/github/Aylur/ags/widget.js';
import Dock from './dock.js';
import { GdkMonitorFromName } from '../../workspace_specific_methods.js';

export default (monitor_name) => Widget.Window({
    gdkmonitor: GdkMonitorFromName(monitor_name),
    name: `dock-${monitor_name}`,
    layer: userOptions.dock.layer,
    anchor: ['bottom'],
    exclusivity: 'normal',
    visible: true,
    child: Dock(monitor_name),
});
