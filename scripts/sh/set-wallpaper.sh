#!/bin/bash

mv -v $1 wallpaper.jpg
cp -v wallpaper.jpg ~/Pictures
sudo cp -v wallpaper.jpg /etc/lightdm/
feh --bg-fill -V wallpaper.jpg
rm wallpaper.jpg
