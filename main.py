from file_helper import get_file
from Obsidian2LaTeX_helper import bake_TeX, convert_MD2TeX


def main(mddir, name):
    get_file()
    convert_MD2TeX(mddir, name)
    bake_TeX(name)


if __name__ == "__main__":
    main()
