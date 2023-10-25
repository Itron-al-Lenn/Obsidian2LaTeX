from file_helper import get_file, save_file
from Obsidian2LaTeX_helper import bake_TeX, convert_MD2TeX


def main():
    name = "Test"
    get_file()
    convert_MD2TeX("C:/Users/jolle/Desktop/Libary/Python/Obsidian2LaTeX/test.md", name)
    save_file()
    bake_TeX(name)


if __name__ == "__main__":
    main()
