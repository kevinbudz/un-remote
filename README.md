# un-remote

A .py script for eliminating the use of remote textures in RotMG private servers. This script contains two main components.
1. **Image processing:** If you open this script in a directory with remote image files, it will try and deduce whether it's a static image, skin, enemy, or mask. After doing so, it'll generate new sprite sheets and place them into their allocated index.
2. **XML Parsing:** If you ALSO have an .xml attached, it will read the .xml, see if a static image has been put into a sprite sheet already, then edit the .xml accordingly to accomodate for the sprite sheet.

## this works with..
- static images,
- enemies,
- skins,
- skin masks.

## you will need..
- python 3.x,
- **'pillow'** libary. `pip install pillow` 

## to use..
1. In **File Explorer**, place this script in the same directory as your remote textures. 
2. If you have an .xml file that corresponds with these remote textures, import it into the same directory.
3. While still in **File Explorer**, click on the bar that shows your directory, highlight it, erase it, and type `cmd`.
4. In the opened **CMD** window, type `python3 main.py` and let it run!

## notes..
- this only automates **MOST** of the process, you are still responsible for adding the sprite sheets to EmbeddedAssets/AssetLoader.as in your client AND fixing any bugs that correspond with importing the sprite sheets.