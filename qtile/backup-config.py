import os
import re
import socket
import subprocess
import current_location
from typing import List  # noqa: F401
from libqtile import layout, bar, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
# Make sure 'qtile-extras' is installed or this config will not work.
from qtile_extras import widget  # type: ignore
from qtile_extras.widget.decorations import BorderDecoration # type: ignore
from libqtile.widget import Spacer


#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

myTerm = "kitty" # OR alacritty
myBrowser = "brave"
border_width = 4

keys = [

# SUPER + FUNCTION KEYS
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "t", lazy.spawn('xterm')),
    Key([mod], "d", lazy.spawn('pcmanfm')),
    Key([mod], "b", lazy.spawn(myBrowser), desc='Web browser'),
    Key([mod], "v", lazy.spawn('pavucontrol')),
    Key([mod], "r", lazy.spawn('rofi -show drun')),
    # Key([mod], "d", lazy.spawn('nwggrid -p -o 0.4')),
    Key([mod], "Escape", lazy.spawn('xkill')),
    Key([mod], "Return", lazy.spawn(myTerm)),
    Key([mod], "KP_Enter", lazy.spawn('alacritty')),
    # Key([mod], "x", lazy.shutdown()),
    Key([mod], "equal", lazy.spawn('rofi -show calc -modi calc -no-show-match -no-sort')),

# SUPER + SHIFT KEYS
    Key([mod, "shift"], "Return", lazy.spawn('pcmanfm')),
    Key([mod, "shift"], "d", lazy.spawn("dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=14'")),
    # Key([mod, "shift"], "d", lazy.spawn(home + '/.config/qtile/scripts/dmenu.sh')),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "shift"], "x", lazy.shutdown()),

# CONTROL + ALT KEYS
    Key(["mod1", "control"], "o", lazy.spawn(home + '/.config/qtile/scripts/picom-toggle.sh')),
    Key(["mod1", "control"], "t", lazy.spawn('xterm')),
    Key(["mod1", "control"], "u", lazy.spawn('pavucontrol')),

# ALT + ... KEYS
    Key(["mod1"], "p", lazy.spawn('pamac-manager')),
    Key(["mod1"], "f", lazy.spawn('firedragon')),
    Key(["mod1"], "m", lazy.spawn('pcmanfm')),
    # Key(["mod1"], "w", lazy.spawn('garuda-welcome')),


# CONTROL + SHIFT KEYS

    Key([mod2, "shift"], "Escape", lazy.spawn('lxtask')),


# SCREENSHOTS

    Key([], "Print", lazy.spawn('flameshot full -p ' + home + '/Pictures')),
    Key([mod2], "Print", lazy.spawn('flameshot full -p ' + home + '/Pictures')),
#    Key([mod2, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),

# MULTIMEDIA KEYS

# INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +3%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 3%- ")),

# INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

#    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
#    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
#    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
#    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),

# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

         ### Treetab controls
    Key([mod, "control"], "k",
        lazy.layout.section_up(),
        desc='Move up a section in treetab'
        ),
    Key([mod, "control"], "j",
        lazy.layout.section_down(),
        desc='Move down a section in treetab'
        ),


# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),]

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
#group_labels = ["", "", "", "", "",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "treetab", "floating",]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for g in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], g.name, lazy.group[g.name].toscreen(toggle=True)),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], g.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], g.name, lazy.window.togroup(g.name) , lazy.group[g.name].toscreen()),
    ])


# COLORS FOR THE BAR


def init_colors():
    return [["#262626", "#262626"], # color 0
            ["#2F343F", "#2F343F"], # color 1
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#fea63c", "#fea63c"], # color 3
            ["#f4c2c2", "#f4c2c2"], # color 4
            ["#c0b18b", "#c0b18b"], # color 5
            ["#FDDA0D", "#FDDA0D"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#ffffff", "#ffffff"], # color 8
            ["#000000", "#000000"], # color 9
            ["#0000ff", "#0000ff"], # color 10
            ["#E143FC", "#E143FC"], #11
            ["#4c566a", "#4c566a"], #12
            ["#282c34", "#282c34"], #13
            ["#212121", "#212121"], #14
            ["#e75480", "#e75480"], #15 
            ["#05DDC2", "#05DDC2"], #16 
            ["#abb2bf", "#abb2bf"], #17
            ["#81a1c1", "#81a1c1"], #18 
            ["#56b6c2", "#56b6c2"], #19 
            ["#C0392B", "#C0392B"], #20
            ["#DD1005", "#DD1005"], #21 
            ["#DD6B05", "#DD6B05"], #22
            ["#ffd47e", "#ffd47e"]] #23

colors = init_colors()

def init_layout_theme():
    return {"margin":5,
            "border_width":border_width,
            "border_focus": colors[3],
            "border_normal": colors[4]
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(margin=8, border_width=border_width, border_focus=colors[3], border_normal=colors[4]),
    layout.MonadWide(margin=8, border_width=border_width, border_focus=colors[3], border_normal=colors[4]),
    # layout.Matrix(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Floating(**layout_theme),
    # layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
    layout.Columns(**layout_theme),
    # layout.Stack(**layout_theme),
    layout.Tile(**layout_theme),
    # layout.TreeTab(
    #     sections=['FIRST', 'SECOND'],
    #     bg_color = '#141414',
    #     active_bg = '#0000ff',
    #     inactive_bg = '#1e90ff',
    #     padding_y =5,
    #     section_top =10,
    #     panel_width = 280),
    # layout.VerticalTile(**layout_theme),
    layout.Zoomy(**layout_theme)
]

def base(fg='text', bg='dark'):
    return {'foreground': colors[14],'background': colors[0]}

# WIDGETS FOR THE BAR

widget_defaults = dict(
    font='Fira Sans',
    fontsize=14,
    background=colors[0],
    foreground=colors[5],
    opacity=1,
    padding=5
)
extension_defaults = widget_defaults.copy()

def init_widgets_defaults():
    return dict(
        font='Fira Sans',
        fontsize=16,
        background=colors[0],
        foreground=colors[5],
        opacity=1,
        padding=10,
        icon_size=30
    )


widget_defaults = init_widgets_defaults()


def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [

        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[0],
            background=colors[0]
        ),

        widget.Image(
            filename="~/.config/qtile/icons/garuda-red.png",
            iconsize=14,
            background=colors[0],
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('jgmenu_run')}
        ),

        widget.GroupBox(
            **base(bg=colors[0]),
            font='UbuntuMono Nerd Font',
            margin_y=4,
            margin_x=2,
            padding_y=2,
            padding_x=4,
            borderwidth=3,
            active=colors[5],
            inactive=colors[12],
            rounded=True,
            # highlight_method = 'line',
            highlight_method='block',
            urgent_alert_method='block',
            urgent_border=colors[6],
            this_current_screen_border=colors[3],
            this_screen_border=colors[17],
            other_current_screen_border=colors[13],
            other_screen_border=colors[17],
            disable_drag=True
        ),

        widget.TaskList(
            highlight_method='block',  # or border
            max_title_width=180,
            rounded=True,
            padding_x=2,
            padding_y=4,
            margin_y=0,
            border=colors[1],
            foreground=colors[5],
            margin=8,
            txt_floating='🗗',
            txt_minimized='> ',
            borderwidth=1,
            background=colors[0],
            unfocused_border = 'border'
        ),

        widget.Volume(
            emoji=False,
            fmt = '🕫  VOL: {}',
            decorations=[
                BorderDecoration(
                    colour = colors[5],
                    border_width = [0, 0, 2, 0],
                )
            ]
        ),

        widget.Net(
            # Here enter your network name
            # interface=["wlp6s0"],
            format='NET: {down} ↓↑ {up}',
            decorations=[
                BorderDecoration(
                    colour = colors[16],
                    border_width = [0, 0, 2, 0],
                )
            ]
        ),

        # widget.CPUGraph(
        #     padding=10,
        # ),

        widget.ThermalSensor(
            format='TEMP: {temp:.0f}{unit}',
            tag_sensor='Core 0',
            threshold=40,
            decorations=[
                BorderDecoration(
                    colour = colors[21],
                    border_width = [0, 0, 2, 0],
                )
            ],
        ),

        widget.CPU(
            format="CPU {load_percent}%",
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')
            },
            decorations=[
                BorderDecoration(
                    colour = colors[21],
                    border_width = [0, 0, 2, 0],
                )
            ],
        ),

        # widget.Moc(),

        # widget.Memory(
        #     # format="{MemUsed: .0f}M/{MemTotal: .0f}M",
        #     update_interval=1,
        #     measure_mem='M',
        #     foreground=colors[5],
        #     background=colors[14],
        #     mouse_callbacks={
        #         'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
        # ),

        # https://openweathermap.org/city/5786899
        widget.OpenWeather(
            app_key = "4cf3731a25d1d1f4e4a00207afd451a2",
            # cityId="5786899",
            coordinates={"longitude": current_location.data["longitude"], "latitude": current_location.data["latitude"]},
            format = '{location_city} Forecast: {icon} {temp}° and {weather_details}. 🌆 {sunset}',
            metric = False,
            decorations=[
                BorderDecoration(
                    colour = colors[22],
                    border_width = [0, 0, 2, 0],
                )
            ],
        ),

        widget.Wallpaper(
            random_selection=False,
            # max_chars=11,
            directory='~/Pictures/wallpapers/',
            label="BG",
            decorations=[
                BorderDecoration(
                    colour = colors[6],
                    border_width = [0, 0, 2, 0],
                )
            ]
        ),

        # widget.CurrentLayout(
        #     font="Noto Sans Bold",
        #     foreground=colors[5],
        #     background=colors[11],
        # ),

        widget.Clock(
            format='%a, %b %d - %I:%M %p',
            font='Noto Sans bold',
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn(myTerm + 'google Google Calendar')
            },
            decorations=[
                BorderDecoration(
                    colour = colors[10],
                    border_width = [0, 0, 2, 0],
                )
            ]
        ),

        # widget.CurrentLayoutIcon(
        #     custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
        #     foreground=colors[5],
        #     # background=colors[22],
        #     padding=0,
        #     scale=0.7,
        #     decorations=[
        #         BorderDecoration(
        #             colour = colors[16],
        #             border_width = [0, 0, 2, 0],
        #         )
        #     ]
        # ),

    widget.Battery (
        format = "🔋{char} {percent:0.1%}",
        update_interval = 3,
        low_percentage = 0.10,
        unknown_char = "",
        full_char = "",
        charge_char = "+",
        discharge_char = "-",
        empty_char = "",
        low_foreground = colors[6],
        decorations=[
            BorderDecoration(
                colour = colors[7],
                border_width = [0, 0, 2, 0],
            )
        ]
    ),

    widget.Systray(
        padding_x=4,
        margin=2,
        icon_size=22
    ),

    ]
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


widgets_screen1 = init_widgets_screen1()


def init_screens():
    return [Screen(
        top=bar.Bar(widgets=init_widgets_screen1(), size=25, opacity=0.85, background="000000"),
        wallpaper_mode='fill',
    )]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules: List[str] = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #########################################################
#     ################ assgin apps to groups ##################
#     #########################################################
#     d["1"] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d["2"] = [ "Atom", "Subl3", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl3", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d["3"] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d["4"] = ["Gimp", "gimp" ]
#     d["5"] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d["6"] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d["7"] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d["8"] = ["pcmanfm", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "pcmanfm", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d["9"] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d["0"] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ##########################################################
#     wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen()

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME



main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(title='branchdialog'),
    Match(title='Open File'),
    Match(title='pinentry'),
    Match(wm_class='ssh-askpass'),
    Match(wm_class='lxpolkit'),
    Match(wm_class='Lxpolkit'),
    Match(wm_class='yad'),
    Match(wm_class='Yad'),
    Match(wm_class='Cairo-dock'),
    Match(wm_class='cairo-dock'),


],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.

wmname = "LG3D"
