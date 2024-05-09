import PopupWindow from '../.widgethacks/popupwindow.js';
import OnScreenKeyboard from "./onscreenkeyboard.js";

export default (monitor_name) => PopupWindow({
    anchor: ['bottom'],
    name: `osk${monitor_name}`,
    showClassName: 'osk-show',
    hideClassName: 'osk-hide',
    child: OnScreenKeyboard({ monitor_name: monitor_name }),
});
