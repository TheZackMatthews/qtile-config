#!/bin/bash

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}



#starting utility applications at boot time
lxsession &
run nm-applet &
run pamac-tray &
numlockx on &
blueman-applet &
#flameshot &
#picom --config $HOME/.config/picom/picom.conf &
picom --config .config/picom/picom-blur.conf --experimental-backends &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
dunst &
feh --randomize --bg-fill ~/Pictures/wallpapers*
#starting user applications at boot time
run volumeicon &
#run discord &
#nitrogen --random --set-zoom-fill &
#run caffeine -a &
#run vivaldi-stable &
run insync start &
run ~/Code/Scripts/city-geolocate.bash
#run spotify &

export QT_SCALE_FACTOR=1.5
