# Obsidian2LaTeX Converter

I am a STEM student who uses obsidian.md for her lecture notes. Because I am deeply unsatisfied with the integrated pdf conversion I decided to write this little program.
It uses the similarity of the MathJax syntax to LaTeX to convert the .md file to a .tex file and convert the .tex file to a stylish-looking pdf using pdflatex.

## What works

It currently supports the following elements:

- Math and align environment
- All MathJax syntax that is identical to LaTeX
- The mhchem \pu (will be converted to \si)Header and first-level subheaders (# and ##)
- bold and italic text (italic with the notation using _)
- Images

## What _doesn't_ work (right now)

These things don't work right now. Either because of some syntax conflict or just because I didn't have time (or saw the need) to add them by now.

- Excalidraw
- Tables
- All math environments that are mutually exclusive to align or \[ (could probably easily be added by reusing the code for align)

## Requirements

- TeX Live
- Inkscape (if you use Excalidraw)
- Excalidraw_export

## How to use

- First, install TeX Live if you don't have it already installed. You can find a guide on how to [here](https://tug.org/texlive/acquire-netinstall.html)](https://tug.org/texlive/acquire-netinstall.html).
- If you want to use Excalidraw also install Inkscape. You find the download [here](https://inkscape.org/release/)
- For Excalidraw support you too need excalidraw_export. You can install it using:

```cmd
npm install -g excalidraw_export
```

<br>
- Download the latest release [here](https://github.com/Itron-al-Lenn/Obsidian2LaTeX/releases)
- Unpack the binary in the directory you want and run it.
- If you want to change the standard inputs you can change the config file you find in:

```path
C:\Users\<username>\AppData\Local\Itron al Lenn\Obsidian2LaTeX
```

## ToDo's

- [x] Convert MD to TeX to pdf
- [X] change content from MD to reflect the syntax of LaTeX
- [X] Make an interface to pick the MD file you want to convert
- [X] Add the option to choose a custom LaTeX template to the interface
- [X] Add support for italic
- [X] Add support for images
- [X] Add support for .excalidraw
