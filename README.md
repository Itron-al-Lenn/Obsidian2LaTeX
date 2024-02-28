# Obsidian2LaTeX Converter

I am a STEM student who uses obsidian.md for her lecture notes. Because I am deeply unsatisfied with the integrated pdf conversion I decided to write this little program.
It uses the similarity of the MathJax syntax to LaTeX to convert the .md file to a .tex file and convert the .tex file to a stylish-looking pdf using MiKTeX.

## What works

It currently supports the following elements:

- Math and align environment
- All MathJax syntax that is identical to LaTeX
- The mhchem \pu (will be converted to \si) Header and first-level subheaders (# and ##)
- bold and italic text (italic with the notation using _)
- Images
- Excalidraw

## What _doesn't_ work (right now)

These things don't work right now. Either because of some syntax conflict or just because I didn't have time (or saw the need) to add them by now.

- Tables
- All math environments that are mutually exclusive to align or \[ (could probably easily be added by reusing the code for align)
- Links

## Requirements

- MiKTeX and latexmk
- Inkscape (if you use Excalidraw)
- Excalidraw_export (if you use Excalidraw)

## How to use

- First, install MiKTeX if you don't have it already installed. You can find the installer on their [website](https://miktex.org/download). Then make sure in the MiKTeX console that you have latexmk installed.
- If you want to use Excalidraw also install Inkscape. You find the download [here](https://inkscape.org/release/)
- For Excalidraw support you too need excalidraw_export. You can install it using:

```cmd
npm install -g excalidraw_export
```

<br><br>

- Download the latest release [here](https://github.com/Itron-al-Lenn/Obsidian2LaTeX/releases)
- Unpack the binary in the directory you want and run it.
- If you want to change the standard inputs you can change the config file you find in:

```path
C:\Users\<username>\AppData\Local\Itron al Lenn\Obsidian2LaTeX
```
