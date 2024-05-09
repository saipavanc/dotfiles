import Widget from 'resource:///com/github/Aylur/ags/widget.js';
import { enableClickthrough } from "../.widgetutils/clickthrough.js";
import { RoundedCorner } from "../.commonwidgets/cairo_roundedcorner.js";
import { GdkMonitorFromName } from '../../workspace_specific_methods.js';

export default (monitor_name, where = 'bottom left', useOverlayLayer = true) => {
    const positionString = where.replace(/\s/, ""); // remove space
    return Widget.Window({
        gdkmonitor: GdkMonitorFromName(monitor_name),
        name: `corner${positionString}-${monitor_name}`,
        layer: useOverlayLayer ? 'overlay' : 'top',
        anchor: where.split(' '),
        exclusivity: 'ignore',
        visible: true,
        child: RoundedCorner(positionString, { className: 'corner-black', }),
        setup: enableClickthrough,
    });
}