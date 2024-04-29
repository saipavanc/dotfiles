import Widget from 'resource:///com/github/Aylur/ags/widget.js';
import { SearchAndWindows } from "./windowcontent.js";
import PopupWindow from '../.widgethacks/popupwindow.js';

export default (id = '') => PopupWindow({
    name: `search${id}`,
    // exclusivity: 'ignore',
    keymode: 'exclusive',
    visible: false,
    anchor: ['top', 'bottom'],
    layer: 'overlay',
    child: Widget.Box({
        vertical: true,
        children: [
            SearchAndWindows(false),
        ]
    }),
})
