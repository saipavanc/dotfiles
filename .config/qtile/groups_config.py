# --------------------------------------------------------
# Custom imports
# --------------------------------------------------------
from defaults import mod
from appearance import ColorsDict

# --------------------------------------------------------
# Groups for Qtile
# --------------------------------------------------------
from libqtile.config import Group, ScratchPad, DropDown, Click, Drag, Match
from libqtile import layout
from libqtile.lazy import lazy
from libqtile.dgroups import simple_key_binder


groups = [Group(i, layout="monadtall") for i in "1234567890"]
dgroups_key_binder = simple_key_binder(mod)

def latest_group(qtile):
    qtile.current_screen.set_group(qtile.current_screen.previous_group)

# --------------------------------------------------------
# Scratchpads
# --------------------------------------------------------

groups += [
    ScratchPad(
            "temp",
                    [
                    DropDown("chatgpt", "brave --app=https://chat.openai.com", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
                    DropDown("mousepad", "mousepad", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
                    DropDown("terminal", "alacritty", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
                    DropDown("scrcpy", "scrcpy -d", x=0.8, y=0.05, width=0.15, height=0.6, on_focus_lost_hide=False )
                    ],
                )
            ]


# --------------------------------------------------------
# Setup Layout Theme
# --------------------------------------------------------

layout_theme = { 
    "border_width": 3,
    "margin": 15,
    "border_focus": ColorsDict["color2"],
    "border_normal": "FFFFFF",
    "single_border_width": 3
}

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------

layouts = [
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Floating()
]


# --------------------------------------------------------
# Drag floating layouts
# --------------------------------------------------------

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# --------------------------------------------------------
# Define floating layouts
# --------------------------------------------------------

floating_layout = layout.Floating(
    border_width=3,
    border_focus=ColorsDict["color2"],
    border_normal="FFFFFF",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
