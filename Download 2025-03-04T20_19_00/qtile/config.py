# qtile config file
import os
import sys
import subprocess
sys.path.append('/nix/store/x1g9xyd5r7qgq9nm5zdz04lkiipfygkp-python3.12-qtile-extras-0.25.0/lib/python3.12/site-packages')

# Make sure 'qtile-extras' is installed or this config will not work.
sys.path.append(os.path.expanduser("~/.config/python"))
#from colors import RoseLinuxDark as colors
from colors import AmyMountain as colors

from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.widget import battery
from libqtile.lazy import lazy

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from keys import keys

##Variables##
mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "firefox"     # My browser of choice
myEmacs = "emacsclient -c -a 'emacs' " # The space at the end is IMPORTANT!
myPrompt = "rofi -show drun"

## The Key binds have been moved to keys.py and are imported ##

groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]

group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]


group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))
 
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )


### COLORSCHEME ###
# Colors are defined in a separate 'colors.py' file.
# There up 12 colorschemes available to choose from
# These include:
#
# colors = colors.DoomOne
# colors = colors.Dracula
# colors = colors.Nord
# colors = colors.OceanicNext
# colors = colors.Palenight
# colors = colors.SolarizedDark
# colors = colors.RoseLinuxDark
#
# It is best not manually change the colorscheme; instead run 'dtos-colorscheme'
# which is set to 'MOD + p c'

colors = colors 

### LAYOUTS ###
# Some settings that I use on almost every layout, which saves us
# from having to type these out for each individual layout.
layout_theme = {"border_width": 5,
                "margin": 10,
                "border_focus": '#8bca84',
                "border_normal": colors[0]
                }

layouts = [
    #layout.Bsp(**layout_theme),
    #layout.Floating(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    #layout.MonadWide(**layout_theme),
    layout.Max(
         border_width = 0,
         margin = 0,
         ),
    #layout.Stack(**layout_theme, num_stacks=2),
    #layout.Columns(**layout_theme),
    layout.TreeTab(
         font = "Ubuntu Bold",
         fontsize = 11,
         border_width = 0,
         bg_color = colors[0],
         active_bg = colors[8],
         active_fg = colors[2],
         inactive_bg = colors[1],
         inactive_fg = colors[0],
         padding_left = 8,
         padding_x = 8,
         padding_y = 6,
         sections = ["ONE", "TWO", "THREE"],
         section_fontsize = 10,
         section_fg = colors[7],
         section_top = 15,
         section_bottom = 15,
         level_shift = 8,
         vspace = 3,
         panel_width = 240
         ),
    layout.Zoomy(**layout_theme),
]

# Some settings that I use on almost every widget, which saves us
# from having to type these out for each individual widget.
widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 12,
    padding = 0,
    background=colors[0]
)

extension_defaults = widget_defaults.copy()

# Before we configure the widgets, we are going to define the battery widget to change based on its 
# charge status

def update_battery(widget):
    battery_info = widget._battery.update_status()
    if battery_info:
        percent = battery_info.percent / 100
        charging = battery_info.status == "Charging"

        if charging:
            widget.foreground = colors[8]
        elif percent < 0.2:
            widget.foreground = colors[5]
        else:
            widget.foreground = colors[3]

def get_volume():
    try:
        # List all sinks
        sinks = subprocess.check_output("pactl list short sinks", shell=True).decode('utf-8').strip().split('\n')
        
        # Identify the correct sink
        target_sink = None
        for sink in sinks:
            if "usb-Framework_Audio_Expansion_Card" in sink:
                target_sink = sink.split()[1]
                break
        
        if target_sink is None:
            return "N/A"  # Return N/A if the sink is not found
        
        # Fetch the volume level
        volume = subprocess.check_output(
            f"pactl get-sink-volume {target_sink} | grep -oP '\\d+%' | head -1",
            shell=True
        ).decode('utf-8').strip()
        
        # Check if muted
        mute = subprocess.check_output(
            f"pactl get-sink-mute {target_sink} | grep -oP 'yes|no'",
            shell=True
        ).decode('utf-8').strip()
        
        if mute == "yes":
            return "M"
        else:
            return volume
    except Exception as e:
        return "N/A"  # Return N/A if there is an error fetching the volume

def init_widgets_list():
    battery_widget = widget.Battery(
        foreground=colors[5],
        foreground_alert=colors[4],
        foreground_charge=colors[8],
        format='{char} {percent:2.1%} {hour:d}:{min:02d}',
        charge_char='CH',
        discharge_char='DS',
        update_interval=10,
        decorations=[
            BorderDecoration(
                colour = colors[5],
                border_width=[0,0,2,0],
             )
         ],
    )
  
    battery_widget.add_callbacks(
            {'Button1': lambda: update_battery(battery_widget)}
        )

    widgets_list = [
        widget.Image(
                 filename = "~/.config/qtile/icons/rose.png",
                 scale = "False",
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myPrompt)},
                 ),
        widget.Prompt(
                 font = "Ubuntu Mono",
                 fontsize=14,
                 foreground = colors[1]
        ),
        widget.GroupBox(
                 fontsize = 11,
                 margin_y = 3,
                 margin_x = 4,
                 padding_y = 2,
                 padding_x = 3,
                 borderwidth = 3,
                 active = colors[7],
                 inactive = colors[1],
                 rounded = False,
                 highlight_color = colors[2],
                 highlight_method = "line",
                 this_current_screen_border = colors[7],
                 this_screen_border = colors [4],
                 other_current_screen_border = colors[7],
                 other_screen_border = colors[4],
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[1],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.CurrentLayoutIcon(
                 # custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                 foreground = colors[1],
                 padding = 0,
                 scale = 0.7
                 ),
        widget.CurrentLayout(
                 foreground = colors[1],
                 padding = 5
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[1],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.WindowName(
                 foreground = colors[6],
                 max_chars = 40
                 ),
#        widget.GenPollText(
#                 update_interval = 300,
#                 func = lambda: subprocess.check_output("printf $(uname -r)", shell=True, text=True),
#                 foreground = colors[3],
#                 fmt = '{}',
#                 decorations=[
#                     BorderDecoration(
#                         colour = colors[3],
#                         border_width = [0, 0, 2, 0],
#                     )
#                 ],
#                 ),
#        widget.Spacer(length = 8),
#        widget.CPU(
#                 format = 'Cpu: {load_percent}%',
#                 foreground = colors[4],
#                 decorations=[
#                     BorderDecoration(
#                         colour = colors[4],
#                         border_width = [0, 0, 2, 0],
#                     )
#                 ],
#                 ),
#        widget.Spacer(length = 8),
#        widget.Memory(
#                 foreground = colors[8],
#                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
#                 format = '{MemUsed: .0f}{mm}',
#                 fmt = 'Mem: {} used',
#                 decorations=[
#                     BorderDecoration(
#                         colour = colors[8],
#                         border_width = [0, 0, 2, 0],
#                     )
#                 ],
#                 ),
        widget.Spacer(length = 8),
        widget.DF(
                 update_interval = 60,
                 foreground = colors[8],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e df')},
                 partition = '/home',
                 #format = '[{p}] {uf}{m} ({r:.0f}%)',
                 format = '{uf}{m} free',
                 fmt = 'Disk: {}',
                 visible_on_warn = False,
                 decorations=[
                     BorderDecoration(
                         colour = colors[8],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.GenPollText(
                 foreground = colors[7],
                 update_interval=1,
                 func=get_volume,
                 fmt = 'Vol: {}',
                 mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('pavucontrol')},
                 decorations=[
                     BorderDecoration(
                         colour = colors[7],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.KeyboardLayout(
                 foreground = colors[3],
                 fmt = 'Keys: {}',
                 decorations=[
                     BorderDecoration(
                         colour = colors[3],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.Clock(
                 foreground = colors[6],
                 format = "%H:%M - %a, %b %d",
                 decorations=[
                     BorderDecoration(
                         colour = colors[6],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        battery_widget, 
        widget.Spacer(length = 8),
        widget.Systray(padding = 3),
        widget.Spacer(length = 8),
        ]
    return widgets_list


# Monitor 1 will display ALL widgets in widgets_list. It is important that this
# is the only monitor that displays all widgets because the systray widget will
# crash if you try to run multiple instances of it.
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1 

# All other monitors' bars will display everything but widgets 22 (systray) and 23 (spacer).
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[20:22]
    return widgets_screen2

# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=30)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=30)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=30))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[8],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),   # gitk
        Match(wm_class="dialog"),         # dialog boxes
        Match(wm_class="download"),       # downloads
        Match(wm_class="error"),          # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class='kdenlive'),       # kdenlive
        Match(wm_class="makebranch"),     # gitk
        Match(wm_class="maketag"),        # gitk
        Match(wm_class="notification"),   # notifications
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        Match(wm_class="ssh-askpass"),    # ssh-askpass
        Match(wm_class="toolbar"),        # toolbars
        Match(wm_class="Yad"),            # yad boxes
        Match(title="branchdialog"),      # gitk
        Match(title='Confirmation'),      # tastyworks exit box
        Match(title='Qalculate!'),        # qalculate-gtk
        Match(title="pinentry"),          # GPG key password entry
        Match(title="tastycharts"),       # tastytrade pop-out charts
        Match(title="tastytrade"),        # tastytrade pop-out side gutter
        Match(title="tastytrade - Portfolio Report"), # tastytrade pop-out allocation
        Match(wm_class="tasty.javafx.launcher.LauncherFxApp"), # tastytrade settings
        Match(wm_class="pavucontrol"), # GUI audio mixer
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])
    qtile.call_later(30, lambda: update_battery(battery_widget))
@hook.subscribe.startup
def start_always():
    subprocess.call(['nitrogen','--restore'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
