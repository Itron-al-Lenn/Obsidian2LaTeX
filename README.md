# Obsidian2LaTeX Convertor

I am a STEM student which uses obsidian.md for her lecture notes. Because I am deeply unsatisfied with the integrated pdf conversion I decided to write this little program.
It uses the similarity of the MathJax syntax to LaTeX to convert the .md file to an .tex file and convert the .tex file to an stylish looking pdf using pdflatex.
## What works

It currently supports the following elements:
- Math and align environment
- All MathJax syntax that is identical to LaTeX
- The mhchem \pu (will be converted to \si)
- Header and first level subheaders (# and ##)
- bold text
## What _doesn't_ work (right now)

These things don't work right now. Either because of some syntax conflict or just because I didn't had time (or saw the need) to add them by now.
- italic and undeline
- images (especially excalidraw)
- tables
- all math environments which are mutually exclusive to align or \[ (could probably easaly be added by reusing the code for align) 
# Requirements 

- TeX Live
# How to use

- First install TeX Live if you don't have it already installed. You can find a guide how to [here](https://tug.org/texlive/acquire-netinstall.html).
<br><br>
- Download the latest release [here](https://github.com/Itron-al-Lenn/Obsidian2LaTeX/releases)
- Unpack the binary in the directory you want and run it.
- If you want to change the standard inputs you can change the config file you finde in:
```path
C:\Users\<username>\AppData\Local\Itron al Lenn\Obsidian2LaTeX
```
# ToDo's

- [x] Convert MD to TeX to pdf
- [X] change content from MD to reflect the syntax of LaTeX
- [X] Make an interface to pick the MD file you want to convert
- [X] Add the option to choose an custom LaTeX template to the interface
- [ ] Add support for images
- [ ] Add support for .excalidraw
- [ ] Add support for italic and underline
