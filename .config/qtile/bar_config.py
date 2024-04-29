from libqtile import bar, widget
from libqtile import qtile


from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.widget.decorations import PowerLineDecoration

# --------------------------------------------------------
# Custom imports
# --------------------------------------------------------
from defaults import home
from appearance import ColorsDict

# --------------------------------------------------------
# Setup Widget Defaults
# --------------------------------------------------------

widget_defaults = dict(
    font="Fira Sans SemiBold",
    fontsize=14,
    padding=3
)
extension_defaults = widget_defaults.copy()

# --------------------------------------------------------
# Decorations
# https://qtile-extras.readthedocs.io/en/stable/manual/how_to/decorations.html
# --------------------------------------------------------

decor_left = {
    "decorations": [
        PowerLineDecoration(
            path="arrow_left"
            # path="rounded_left"
            # path="forward_slash"
            # path="back_slash"
        )
    ],
}

decor_right = {
    "decorations": [
        PowerLineDecoration(
            path="arrow_right"
            # path="rounded_right"
            # path="forward_slash"
            # path="back_slash"
        )
    ],
}

# --------------------------------------------------------
# Widgets
# --------------------------------------------------------

widget_list = [
    widget.TextBox(
        **decor_left,
        background=ColorsDict["color1"]+".4",
        text='Apps',
        foreground='ffffff',
        desc='',
        padding=10,
        mouse_callbacks={"Button1": lambda: qtile.spawn("rofi -show drun")},
    ),
    widget.TextBox(
        **decor_left,
        background="#ffffff.4",
        text="  ",
        foreground="000000.6",
        fontsize=18,
        mouse_callbacks={"Button1": lambda: qtile.spawn(home + "/dotfiles/qtile/scripts/wallpaper.sh select")},
    ),
    widget.GroupBox(
        **decor_left,
        background="#ffffff.7",
        highlight_method='block',
        highlight='ffffff',
        block_border='ffffff',
        highlight_color=['ffffff','ffffff'],
        block_highlight_text_color='000000',
        foreground='ffffff',
        rounded=False,
        this_current_screen_border='ffffff',
        active='ffffff'
    ),
    widget.TextBox(
        **decor_left,
        background="#ffffff.4",
        text=" ",
        foreground="000000.6",
        fontsize=18,
        mouse_callbacks={"Button1": lambda: qtile.spawn("bash " + home + "/dotfiles/.settings/browser.sh")},
    ),
    widget.TextBox(
        **decor_left,
        background="#ffffff.4",
        text=" ",
        foreground="000000.6",
        fontsize=18,
        mouse_callbacks={"Button1": lambda: qtile.spawn("bash " + home + "/dotfiles/.settings/filemanager.sh")}
    ),
    
    widget.WindowName(
        **decor_left,
        max_chars=50,
        background=ColorsDict["color2"]+".4",
        width=400,
        padding=10
    ),
    widget.Spacer(),
    widget.Spacer(
        length=30
    ),
    widget.TextBox(
        **decor_right,
        background="#000000.3"      
    ),    
    widget.Memory(
        **decor_right,
        background=ColorsDict["color10"]+".4",
        padding=10,        
        measure_mem='G',
        format="{MemUsed:.0f}{mm} ({MemTotal:.0f}{mm})"
    ),
    widget.Volume(
        **decor_right,
        background=ColorsDict["color12"]+".4",
        padding=10, 
        fmt='Vol: {}',
    ),
    # widget.DF(
    #     **decor_right,
    #     padding=10, 
    #     background=ColorsDict["color8"]+".4",        
    #     visible_on_warn=False,
    #     format="{p} {uf}{m} ({r:.0f}%)"
    # ),
    # widget.Bluetooth(
    #     **decor_right,
    #     background=ColorsDict["color2"]+".4",
    #     padding=10,
    #     mouse_callbacks={"Button1": lambda: qtile.spawn("blueman-manager")},
    # ),
    widget.Systray(
        **decor_right,
        background=ColorsDict["color2"]+".4",
        padding=10,
        icon_size=18,
        ),
    # widget.Wlan(
    #     **decor_right,
    #     background=Color2+".4",
    #     padding=10,
    #     format='{essid} {percent:2.0%}',
    #     mouse_callbacks={"Button1": lambda: qtile.spawn("terminology -e nmtui")},
    # ),
    # widget.Battery(
    #     **decor_right,
    #     battery=0,
    #     background=ColorsDict["color2"]+".4",
    #     padding=10,
    #     format='{char} {percent:2.0%} {hour:d}:{min:02d} {watt:.2f} W',
    #     # mouse_callbacks={"Button1": lambda: qtile.spawn("")},
    #     ),
    widget.Clock(
        **decor_right,
        background=ColorsDict["color4"]+".4",   
        padding=10,      
        format="%Y-%m-%d / %I:%M %p",
    ),
    widget.TextBox(
        **decor_right,
        background=ColorsDict["color2"]+".4",     
        padding=5,    
        text=" ",
        fontsize=20,
        mouse_callbacks={"Button1": lambda: qtile.spawn(home + "/dotfiles/qtile/scripts/powermenu.sh")},
    ),
]


top_bar = bar.Bar(
			widget_list,
			30,
			padding=20,
			opacity=0.7,
			border_width=[0, 0, 0, 0],
			margin=[0,0,0,0],
			background="#000000.3"
		)