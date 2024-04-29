const { Gdk } = imports.gi;

export function setupCursorHover(button) { // Hand pointing cursor on hover
    const display = Gdk.Display.get_default();
    button.connect('enter-notify-event', () => {
        const cursor = Gdk.Cursor.new_from_name(display, 'pointer');
        button.get_window().set_cursor(cursor);
    });

    button.connect('leave-notify-event', () => {
        const cursor = Gdk.Cursor.new_from_name(display, 'default');
        button.get_window().set_cursor(cursor);
    });

}

export function setupCursorHoverAim(button) { // Crosshair cursor on hover
    button.connect('enter-notify-event', () => {
        const display = Gdk.Display.get_default();
        const cursor = Gdk.Cursor.new_from_name(display, 'crosshair');
        button.get_window().set_cursor(cursor);
    });

    button.connect('leave-notify-event', () => {
        const display = Gdk.Display.get_default();
        const cursor = Gdk.Cursor.new_from_name(display, 'default');
        button.get_window().set_cursor(cursor);
    });
}

export function setupCursorHoverGrab(button) { // Hand ready to grab on hover
    button.connect('enter-notify-event', () => {
        const display = Gdk.Display.get_default();
        const cursor = Gdk.Cursor.new_from_name(display, 'grab');
        button.get_window().set_cursor(cursor);
    });

    button.connect('leave-notify-event', () => {
        const display = Gdk.Display.get_default();
        const cursor = Gdk.Cursor.new_from_name(display, 'default');
        button.get_window().set_cursor(cursor);
    });
}

export function setupCursorHoverInfo(button) { // "?" mark cursor on hover
    const display = Gdk.Display.get_default();
    button.connect('enter-notify-event', () => {
        const cursor = Gdk.Cursor.new_from_name(display, 'help');
        button.get_window().set_cursor(cursor);
    });

    button.connect('leave-notify-event', () => {
        const cursor = Gdk.Cursor.new_from_name(display, 'default');
        button.get_window().set_cursor(cursor);
    });
}

export function isCursorHovering(button) { // Check if cursor is hovering over button
    button.connect('enter-notify-event', () => {
        return true;
    });

    button.connect('leave-notify-event', () => {
        return false;
    });
    // let [x, y] = button.get_pointer();
    // let [bx, by, bw, bh] = button.get_allocation();
    // return x >= bx && x <= bx + bw && y >= by && y <= by + bh;
}
