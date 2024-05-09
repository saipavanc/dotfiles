import Widget from 'resource:///com/github/Aylur/ags/widget.js';
import Indicator from '../../services/indicator.js';
import IndicatorValues from './indicatorvalues.js';
import MusicControls from './musiccontrols.js';
import ColorScheme from './colorscheme.js';
import NotificationPopups from './notificationpopups.js';
import { GdkMonitorFromName } from '../../workspace_specific_methods.js';

export default (monitor_name) => Widget.Window({
    name: `indicator-${monitor_name}`,
    gdkmonitor: GdkMonitorFromName(monitor_name),
    className: 'indicator',
    layer: 'overlay',
    // exclusivity: 'ignore',
    visible: true,
    anchor: ['top'],
    child: Widget.EventBox({
        onHover: () => { //make the widget hide when hovering
            Indicator.popup(-1);
        },
        child: Widget.Box({
            vertical: true,
            className: 'osd-window',
            css: 'min-height: 2px;',
            children: [
                IndicatorValues(),
                MusicControls(),
                NotificationPopups(),
                ColorScheme(),
            ]
        })
    }),
});

