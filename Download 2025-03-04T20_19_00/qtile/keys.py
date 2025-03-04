## Keybinds for qtile/config.py ##

# Make sure 'qtile-extras' is installed or this config will not work.
from libqtile.config import Key, KeyChord
from libqtile.lazy import lazy
from libqtile import qtile

mod = "mod4"  # Sets mod key to SUPER/WINDOWS
myTerm = "kitty"  # My terminal of choice
myBrowser = "firefox"  # My browser of choice
myEmacs = "emacsclient -c -a 'emacs' "  # The space at the end is IMPORTANT!
myLogout = "~/Scripts/rofi-power-menu/rofi-power-menu.sh"  # Rofi logout menu script


@lazy.layout.function
def add_treetab_section(layout):
    prompt = qtile.widgets_map["prompt"]
    prompt.start_input("Section name: ", layout.cmd_add_section)

@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()

keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "p", lazy.spawn("rofi -show drun"), desc='Run Launcher'),
    Key([mod], "b", lazy.spawn(myBrowser), desc='Web browser'),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.spawn("/home/anakin/Scripts/rofi-power-menu/rofi-power-menu.sh"), desc="Power menu"),
   # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        lazy.layout.move_left().when(layout=["treetab"]),
        desc="Move window to the left/move tab left in treetab"),

    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        lazy.layout.move_right().when(layout=["treetab"]),
        desc="Move window to the right/move tab right in treetab"),

    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down().when(layout=["treetab"]),
        desc="Move window down/move down a section in treetab"
    ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up().when(layout=["treetab"]),
        desc="Move window downup/move up a section in treetab"
    ),

    # Toggle between split and unsplit sides of stack.
    Key([mod, "shift"], "space", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Treetab prompt
    Key([mod, "shift"], "a", add_treetab_section, desc='Prompt to add new section in treetab'),

    # Grow/shrink windows left/right. 
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),

    # Grow windows up, down, left, right.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.layout.maximize(), desc='Toggle between min and max sizes'),
    Key([mod], "t", lazy.window.toggle_floating(), desc='toggle floating'),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),
    Key([mod], "comma", lazy.prev_screen(), desc='Move focus to prev monitor'),

    # Emacs programs launched using the key chord CTRL+e followed by 'key'
    KeyChord([mod], "e", [
        Key([], "e", lazy.spawn(myEmacs), desc='Emacs Dashboard'),
        Key([], "a", lazy.spawn(myEmacs + "--eval '(emms-play-directory-tree \"~/Music/\")'"), desc='Emacs EMMS'),
        Key([], "b", lazy.spawn(myEmacs + "--eval '(ibuffer)'"), desc='Emacs Ibuffer'),
        Key([], "d", lazy.spawn(myEmacs + "--eval '(dired nil)'"), desc='Emacs Dired'),
        Key([], "i", lazy.spawn(myEmacs + "--eval '(erc)'"), desc='Emacs ERC'),
        Key([], "s", lazy.spawn(myEmacs + "--eval '(eshell)'"), desc='Emacs Eshell'),
        Key([], "v", lazy.spawn(myEmacs + "--eval '(vterm)'"), desc='Emacs Vterm'),
        Key([], "w", lazy.spawn(myEmacs + "--eval '(eww \"distro.tube\")'"), desc='Emacs EWW'),
        Key([], "F4", lazy.spawn("killall emacs"),
             lazy.spawn("/usr/bin/emacs --daemon"),
             desc='Kill/restart the Emacs daemon')
    ]),

    # Key chords to start the specified run prompt in myPrompt
   # KeyChord([mod], "p", [
   #     Key([], "a", lazy.spawn("rofi -show run"), desc='Show Rofi Run'),
   #     Key([], "p", lazy.spawn("rofi -show drun"), desc='Show Rofi Drun'),
   #     Key([], "w", lazy.spawn("rofi -show window"), desc='Show Rofi Window'),
   #     Key([], "k", lazy.spawn("rofi -show keys"), desc='Rofi Keybindings'),
   #     Key([], "n", lazy.spawn("rofi -show notes"), desc='Rofi Notes'),
   #     Key([], "h", lazy.spawn("rofi -show pass"), desc='Rofi Passwords'),
   #     Key([], "s", lazy.spawn("rofi -show search"), desc='Rofi Search'),
   # ]),
]
