# un-remote

A .py script for RotMG server owners. The premise being, if you have a server that consists primarily of remote textures, you can run this script in the same directory and it'll combine all the sprites into multiple sprite sheets.

## this works with..
- static images,
- enemies,
- skins,
- skin masks.

## you will need..
- python 3.x,
- 'pillow' libary (pip install pillow). 

## to use..
1. In File Explorer, place this script in the same directory as your remote textures. 
2. In the bar that shows your directory, highlight it, delete it, and type 'cmd'.
3. Type `python3 main.py` in the opened CMD window, and let it run!

## notes..
- this only automates MOST of the process, you are still responsible for editing all the .xml's to account for the fact these items/enemies/skins are in different sprite sheets.
[](https://i.imgur.com/Lzm3WNE.png)
