# ASCII Image Converter
The program displays raster images using ASCII characters.

# Dependences
* Python3.8
* pillow (`pip3 install pillow`)

# Install
## Linux
> You must have Python3.8 and Git installed
1. `pip3 install pillow`
2. `git clone https://github.com/DarkSeriusCode/ASCII-image`
3. `cd ASCII-image`

# Usage
`python3 img.py [-h] [-r RESIZE] [--symbols SYMBOLS] [--no-print] file`

+ `-r` -- Sets the image compression multiplier and also compresses the input image and saves 						it as `result.jpg`. The compression multiplier indicates how many times the image is compressed. For example: if the compression multiplier is 2, and the image size is 500x500px, then the program will compress the image to a size of 250x2500px.

+ `--symbols` -- Sets valid characters. Image pixels will be replaced with these characters. Index replacement character is calculated by the formula `color_code // (255 // symbols)`, where color_code is the arithmetic mean of all the colors of the pixel.

+ `--no-print` -- The image will be not display if this option selected.